from crypt import methods
from curses import flash
from fileinput import filename
from re import U, template
import re
from tabnanny import filename_only
from flask import Flask, flash, request, redirect, url_for
import redis
import os
from werkzeug.utils import secure_filename
import tempfile
import datetime

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

@app.route('/', methods=['POST', 'GET'])
def upload_file():
    # ポストのリクエストを受け取った時に処理を動かす
    if request.method == 'POST':
          
        # リクエストの中にファイルがあるかを確認する
        if 'file' not in request.files:
              # リダイレクトさせる処理（以下省略）
              return redirect(request.url)
        # ファイルが含まれる時は、file に値を格納する
        file = request.files['file']

        # ファイルの名前が空白出ないかを確認する
        if file.filename == '':
            return redirect(request.url)
        
        # file がしっかり存在し、filename の拡張子が問題ない場合、処理を動かす
        if file and allowed_file(file.filename):
              # 危険な文字を削除する
              filename = secure_filename(file.filename)
              # 問題なければファイルを/tmp ディレクトリに保存する
              file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
              return redirect(request.url)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
