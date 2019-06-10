from flask import Flask, request, send_from_directory, jsonify, make_response
from flask_cors import CORS
import os
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config.from_envvar('APP_CONFIG_FILE')
app.config['STORAGE_PORT'] = os.environ.get('STORAGE_PORT')
app.config['UPLOAD_FOLDER'] = "/app/images"#+app.config['STORAGE_PORT']
jwt = JWTManager(app)
CORS(app)


@app.route('/')
def index():
    return "Hello from ~Storage Server"


@app.route('/post_image', methods=['POST'])
def post_image():
    file = request.files['file']

    assert os.path.exists(app.config['UPLOAD_FOLDER']) == True

    try:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        assert os.path.exists('/app/images/'+file.filename) == True
        return make_response(jsonify('OK'), 201)
    except:
        return make_response(jsonify('failed'), 400)


@app.route('/uploads/<filename>')
def get_uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
