from .routes import api_blueprint
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

app.config.from_envvar('APP_CONFIG_FILE')

CORS(app)
app.register_blueprint(api_blueprint)
