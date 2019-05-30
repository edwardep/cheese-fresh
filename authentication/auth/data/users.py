# import datetime
# from flask_mongoengine import MongoEngine
# from .. import app
# from application.data.galleries import Gallery

# db = MongoEngine(app)


# class User(db.Document):
#     registered_date = db.DateTimeField(default=datetime.datetime.now)
#     profile_image = db.StringField()
#     username = db.StringField(required=True, unique=True)
#     email = db.StringField(required=True, unique=True)
#     password = db.StringField(required=True)
#     followers = db.ListField()
#     following = db.ListField()
#     galleries = db.EmbeddedDocumentListField(Gallery)

#     meta = {
#         # 'db_alias': 'core',
#         'collection': 'users'
#     }
