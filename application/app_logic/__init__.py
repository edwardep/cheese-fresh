from flask import Flask
from flask_cors import CORS
from os import environ
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config.from_envvar('APP_CONFIG_FILE')
app.config['MONGODB_HOST'] = environ.get('MONGODB_HOST')

db = MongoEngine(app)
jwt = JWTManager(app)

CORS(app)
from .routes import api_blueprint
app.register_blueprint(api_blueprint)
