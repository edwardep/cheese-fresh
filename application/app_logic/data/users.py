import datetime
from flask_mongoengine import MongoEngine
from .. import app

db = MongoEngine(app)


class User(db.Document):
    registered_date = db.DateTimeField(default=datetime.datetime.now)
    profile_image = db.StringField()
    username = db.StringField(required=True, unique=True)
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)

    meta = {
        # 'db_alias': 'core',
        'collection': 'users'
    }
