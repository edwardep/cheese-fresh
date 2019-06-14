from flask import Flask, request, send_from_directory, jsonify, make_response
from flask_cors import CORS
import os
from flask_jwt_extended import JWTManager, jwt_required
from kazoo.client import KazooClient
app = Flask(__name__)

app.config.from_envvar('APP_CONFIG_FILE')
app.config['STORAGE_ID'] = os.environ.get('STORAGE_ID')
app.config['UPLOAD_FOLDER'] = "/app/images"#+app.config['STORAGE_PORT']
app.config['ZK_HOST'] = os.environ.get('ZK_HOST')
jwt = JWTManager(app)
CORS(app)

print(app.config['ZK_HOST'])

client = KazooClient(hosts=app.config['ZK_HOST'])
#client = KazooClient(hosts='localhost:2181')
client.start()
client.ensure_path("/storage")


@app.route('/')
def index():
    return "Hello from ~Storage Server"


@app.route('/post_image', methods=['POST'])
#@jwt_required
def post_image():
    file = request.files['file']
    assert os.path.exists(app.config['UPLOAD_FOLDER']) == True

    try:

        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)
        assert os.path.exists(path) == True
        return make_response(jsonify(path), 201)
    except:
        return make_response(jsonify('failed'), 400)

@app.route('/delete_image', methods=['DELETE'])
#@jwt_required
def delete_image():

    filename = request.json['filename']

    #assert os.path.exists(app.config['UPLOAD_FOLDER']) == True
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    #assert os.path.exists(path) == True
    if os.path.exists(path):
        os.remove(path)
        return make_response(jsonify(path), 204)
    else:
        return make_response(jsonify(path), 400)



@app.route('/<filename>')
def get_uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if not client.exists('/storage/'+app.config['STORAGE_ID']):
    client.create('/storage/'+app.config['STORAGE_ID'], b"1000", ephemeral=True)
