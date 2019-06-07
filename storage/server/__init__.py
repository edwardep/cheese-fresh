from flask import Flask, request, send_from_directory, jsonify, make_response
from flask_cors import CORS
from os import environ
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config.from_envvar('APP_CONFIG_FILE')
app.config['STORAGE_PORT'] = environ.get('STORAGE_PORT')
app.config['UPLOAD_FOLDER'] = "/app/media"+app.config['STORAGE_PORT']
jwt = JWTManager(app)
CORS(app)


@app.route('/')
def index():
    return "Hello from ~Storage Server"


@app.route('/post_image', methods=['POST'])
def post_image():
    file = request.files['file']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return make_response(jsonify('OK'), 201)


@app.route('/uploads/<filename>')
def get_uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
