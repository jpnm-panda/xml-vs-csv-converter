from crypt import methods
from fileinput import filename
from re import U, template
from flask import Flask, render_template, request, make_response, jsonify, send_file
import redis
import os
import werkzeug
import tempfile
import datetime


app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!!'
