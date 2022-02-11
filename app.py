from base64 import encode
from crypt import methods
from curses import flash
from fileinput import filename
from pickle import TRUE
from re import U, template
import re
from tabnanny import filename_only
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
import redis
import os
from werkzeug.utils import secure_filename
import tempfile
import datetime
import pandas as pd
from lxml import etree

# ファイルは永続的に保存しないので、保存先は/tmp にする
UPLOAD_FOLDER = '/tmp'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

@app.route('/')
def upload_view():
     return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():    
    # file にPOST された値を格納する
    file = request.files['file']
        
    # 受けとったファイルの値が存在しない場合は、リダイレクトする
    if existing_file(file) and allowed_file(file.filename):
        # 危険な文字を削除する
        filename = secure_filename(file.filename)

        # 問題なければファイルを/tmp ディレクトリに保存する
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(request.url)
    else:
        return redirect(request.url) # 後でエラー用の処理をつくるが、ひとまずリダイレクトにしておく    

@app.route('/data/download')
def download():
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER']), 'conversion-test.csv', as_attachment=True)
        