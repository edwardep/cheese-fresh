from server import app
# from app_logic.data.users import User
# from app_logic.data.galleries import Gallery
import pytest
import os
# from mongoengine import connect
UPLOAD_DIR = '/app/images'

@pytest.fixture
def client():
    client = app.test_client()

    #rm_files_from(UPLOAD_DIR)
    yield client
    rm_files_from(UPLOAD_DIR)


def rm_files_from(path):
    try:
        count = 0
        filelist = [f for f in os.listdir(path)]
        for f in filelist:
            os.remove(os.path.join(path, f))
            count = count + 1
        print('files removed:', format(count))
    except:
        print('failed to rm files')


@pytest.fixture
def utility():
    return Utility


class Utility:
    @staticmethod
    def mock_token():
        # identity = user
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NTk4MTY1OTEsIm5iZiI6MTU1OTgxNjU5MSwianRpIjoiNDdlOWI5YTMtODEwNC00MDNjLTg0MjgtMTQyZTVmOGMwNDkxIiwiZXhwIjoxNTYwODE2NTkxLCJpZGVudGl0eSI6InVzZXIiLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.7BBLbo3-1nUGNn-oEsHRPNbZHpRmmgN5pRJvFAaaI6s'
        return [('Authorization', 'Bearer ' + token)]

#     @staticmethod
#     def mock_user(username):
#         user = User()
#         user.username = username
#         user.password = 'very_secret_password'
#         user.email = username+'@email.com'
#         user.save()

#     @staticmethod
#     def mock_gallery(title):
#         user = User.objects(username='user').first()
#         gallery = Gallery()
#         gallery.title = title
#         gallery.owner = user.username
#         user.galleries.insert(0, gallery)
#         user.save()
