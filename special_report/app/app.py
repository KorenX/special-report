from flask import Flask, request, render_template

import urllib.request as urllib
import base64
from flask import jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify('Index Page')

@app.route('/hello')
def hello():
    return jsonify('Hello, World')

def fill_in_data(data, addr):
    with open('imageToSave_' + addr + '.png', 'wb') as fh:
        fh.write(base64.decodebytes(data))
    return 'goodbye'

def show_the_dog():
    img_url = 'https://www.pythonanywhere.com/user/SpecialReport/files/home/SpecialReport/imageToSave_10.0.0.162.png'
    return render_template("index.html", user_image = img_url)

@app.route('/photo', methods=['GET', 'POST'])
def photo():
    if request.method == 'POST':
        return fill_in_data(request.data, request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
    else:
        return show_the_dog()
