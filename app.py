from ast import Num
from base64 import encode
from crypt import methods
from curses import flash
from fileinput import filename
from pickle import TRUE
from re import U, template
import re
from tabnanny import filename_only
from flask import Flask, flash, request, redirect, url_for, render_template, send_file, send_from_directory
import redis
import os
from werkzeug.utils import secure_filename
import tempfile
import datetime
import pandas as pd
from lxml import etree

# ファイルは永続的に保存しないので、保存先は/tmp にする
UPLOAD_FOLDER = '/tmp'
UPLOAD_FILE_PATH = '/tmp/upload.xml'
CONVERTED_FILE_PATH = '/tmp/converted.csv'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CONVERTED_FILE_PATH'] = CONVERTED_FILE_PATH

# XML とCSV の以外の拡張子は扱わない
ALLOWED_EXTENSIONS = {'xml', 'csv'}

# filename の拡張子を確認するために使う
def allowed_file(filename):
    # ファイルの拡張子が.xml, .csv なら1 をそれ以外なら0を返す
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# file の存在をチャックするため
def existing_file(file):
    # リクエストの中にファイルがあるかとファイル名が空白でないかを確認する
   return False if file not in request.files and file.filename == '' else True

def rm_file(): 
    if os.path.isfile('/tmp/upload.xml'):
        os.remove('/tmp/upload.xml')

    if os.path.isfile('/tmp/converted.csv'):
        os.remove('/tmp/converted.csv')
            

@app.route('/')
def upload_view():
     return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
    rm_file()
    # file にPOST された値を格納する
    file = request.files['file']
        
    # 受けとったファイルの値が存在しない場合は、リダイレクトする
    if existing_file(file) and allowed_file(file.filename):
        # 保存するファイル名を固定する
        filename = 'upload.xml'

        # 問題なければファイルを/tmp ディレクトリに保存する
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(request.url)
    else:
        return redirect(request.url) # 後でエラー用の処理をつくるが、ひとまずリダイレクトにしておく    

@app.route('/data/download')
def download():
     #ファイルがアップロードされている時のみ処理を回す
    if os.path.isfile('/tmp/upload.xml'):
        # XML を読み込んでデータフレームに変換する
        df_read_xml = pd.read_xml('/tmp/upload.xml', encoding='utf-8')

        # データフレーム をCSV に変換する
        df_read_xml.to_csv('/tmp/converted.csv', encoding='utf-8', index=False)
        
        @after_this_request
        def remove_file(response):
            if os.path.isfile('/tmp/upload.xml'):
               os.remove('/tmp/upload.xml')
            return response 

         # 変換したCSV をクライアント側から保存させる
        return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER']), 'converted.csv', as_attachment=True)
    else:
        # ファイルが無い時はルートパスへリダイレクトする
        return redirect('/')
