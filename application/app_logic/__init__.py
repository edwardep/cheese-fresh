from flask import Flask
from flask_cors import CORS
from os import environ
from kazoo.client import KazooClient
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config.from_envvar('APP_CONFIG_FILE')
app.config['MONGODB_HOST'] = environ.get('MONGODB_HOST')
app.config['ZK_HOST'] = environ.get('ZK_HOST')
STORAGE_HOST = environ.get('STORAGE_HOST')
db = MongoEngine(app)
jwt = JWTManager(app)


zk_app = KazooClient(hosts=app.config['ZK_HOST'])
zk_app.start()
zk_app.ensure_path("/app")


def zk_get_storage_children():
    zk_children = zk_app.get_children('/storage')
    count = 0
    for each in zk_children:
        if zk_app.exists("/storage/" + each):
            count = count+1
    return count
    

CORS(app)
from .routes import api_blueprint
app.register_blueprint(api_blueprint)
