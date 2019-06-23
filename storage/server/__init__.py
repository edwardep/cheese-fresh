from flask import Flask, request, send_from_directory, jsonify, make_response
from flask_cors import CORS
import os
from flask_jwt_extended import JWTManager, jwt_required
from kazoo.client import KazooClient
from multiprocessing import Value

count_post_requests = Value('i', 0)
count_get_requests = Value('i', 0)
count_delete_requests = Value('i', 0)

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

if not client.exists('/storage/'+app.config['STORAGE_ID']):
    client.create('/storage/'+app.config['STORAGE_ID'], b"1000", ephemeral=True)

@app.route('/')
def index():
    return "Hello from ~Storage Server "+app.config['STORAGE_ID']+"\n"


@app.route('/post_image', methods=['POST'])
#@jwt_required
def post_image():
    with count_post_requests.get_lock():
        count_post_requests.value += 1
    with open('Output.txt', 'r') as file:
    # read a list of lines into data
        data = file.readlines()
    data.insert(0, "Post requests count: "+str(count_post_requests.value)+"\n")
    with open('Output.txt', 'w') as file:
        file.writelines( data )

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
    with count_delete_requests.get_lock():
        count_delete_requests.value += 1
    with open('Output.txt', 'r') as file:
    # read a list of lines into data
        data = file.readlines()
    data.insert(2,"Delete requests count: "+str(count_delete_requests.value)+"\n")
    with open('Output.txt', 'w') as file:
        file.writelines( data )
    
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
    with count_get_requests.get_lock():
        count_get_requests.value += 1
    with open('Output.txt', 'r') as file:
    # read a list of lines into data
        data = file.readlines()
    data.insert(1,"Get requests count: "+str(count_get_requests.value)+"\n")
    with open('Output.txt', 'w') as file:
        file.writelines( data )
    
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers[
        'Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS, DELETE'
    response.headers[
        'Access-Control-Allow-Headers'] = 'Access-Control-Allow-Origin'
    response.headers[
        'Access-Control-Expose-Headers'] = 'Authorization, Headers, error'
    response.headers['Content-Type'] = 'application/json, multipart/form-data'

    return response