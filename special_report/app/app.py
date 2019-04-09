from flask import Flask, request, render_template
import urllib.request as urllib
import base64
from flask import jsonify

from special_report.ml.image_handler import image_handler
from special_report.app.proccess import proccess_frame
from special_report.db.SpecialReport import DB_GetReport

app = Flask(__name__)

handler = image_handler()
handler.init()


@app.route('/')
def index():
    return jsonify('Index Page')


@app.route('/hello')
def hello():
    return jsonify('Hello, World')


def fill_in_data(data, addr):
    print("Sending from", addr)

    with open('imageToSave_' + addr + '.jpg', 'wb') as fh:
        fh.write(base64.decodebytes(data))

    proccess_frame(handler, path='imageToSave_' + addr + '.jpg')

    return 'goodbye'


@app.route('/photo', methods=['POST'])
def photo():
    return fill_in_data(request.data, request.environ.get('HTTP_X_REAL_IP', request.remote_addr))


@app.route('/report', methods=['GET'])
def report():
    return jsonify([DB_GetReport('050111110'), DB_GetReport('972525848125')])
