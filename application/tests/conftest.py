from app_logic import app
from kazoo.client import KazooClient
from app_logic import zk_app
from app_logic.data.users import User
from app_logic.data.galleries import Gallery
from app_logic.data.images import Image
from app_logic.data.comments import Comment
import pytest
import os
from app_logic import zk_get_storage_children
from mongoengine import connect
from flask_jwt_extended import create_access_token

test_get = True

@pytest.fixture
def client():
    client = app.test_client()
    db = connect('cheese-test')
    db.drop_database('cheese-test')

    yield client
    db.drop_database('cheese-test')


@pytest.fixture
def get_zk_children():
    get_zk_children = zk_get_storage_children()
    yield get_zk_children

@pytest.fixture
def mock_zk_storage():
    mock_zk_storage = KazooClient(hosts=os.environ.get('ZK_HOST'))
    mock_zk_storage.start()
    for i in range(10):
        if not mock_zk_storage.exists('/storage/child'+str(i)):
            mock_zk_storage.create('/storage/child'+str(i), b"1000")
   # mock_zk_storage.create('/storage/child', b"1000")
    yield mock_zk_storage
    #mock_zk_storage.delete('/storage', recursive=True)  
    mock_zk_storage.stop()

@pytest.fixture
def delete_zk_storage_children(mock_zk_storage):
   
    for i in range(3):
        if mock_zk_storage.exists('/storage/child'+str(i)):
            mock_zk_storage.delete('/storage/child'+str(i))
    yield delete_zk_storage_children


@pytest.fixture
def real_zk_app():
    real_zk_app = KazooClient(hosts=os.environ.get('ZK_HOST'))
    yield real_zk_app

@pytest.fixture
def utility():
    return Utility

@pytest.fixture
def mock_add_comment():
    return Utility.mock_add_comment


class Utility:
    @staticmethod
    def mock_token():
        # identity = user
        # username = 'user'
        # token = create_access_token(identity=username)
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1NTk4MTY1OTEsIm5iZiI6MTU1OTgxNjU5MSwianRpIjoiNDdlOWI5YTMtODEwNC00MDNjLTg0MjgtMTQyZTVmOGMwNDkxIiwiZXhwIjoxNTYwODE2NTkxLCJpZGVudGl0eSI6InVzZXIiLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.7BBLbo3-1nUGNn-oEsHRPNbZHpRmmgN5pRJvFAaaI6s'
        return [('Authorization', 'Bearer ' + token)]

    @staticmethod
    def mock_user(username):
        user = User()
        user.username = username
        user.password = 'very_secret_password'
        user.email = username+'@email.com'
        user.save()

    @staticmethod
    def mock_gallery(username, title):
        user = User.objects(username=username).first()
        gallery = Gallery()
        gallery.title = title
        gallery.owner = user.username
        user.galleries.insert(0, gallery)
        user.save()

    @staticmethod
    def mock_follow(user1, user2):
        me = User.objects(username=user1).first()
        friend = User.objects(username=user2).first()
        friend.followers.append(user1)
        friend.save()
        me.following.append(user2)
        me.save()

    @staticmethod
    def mock_add_image(owner, filename):
        image = Image()
        image.path = '/uploads/'+filename
        image.owner = owner
        image.save()
        image.iid = str(image.id)
        image.save()
        me = User.objects(username=owner).first()
        emb_gallery = me.galleries[0]
        emb_gallery.images.insert(0, image.iid)
        me.save()
        return image.iid

    @staticmethod
    def mock_add_comment(owner, iid, text):
        me = User.objects(username=owner).first()
        comment = Comment()
        comment.owner = owner
        comment.text = text
        comment._id = 'super_unique_id'
        image = Image.objects(iid=iid).first()
        image.comments.append(comment)
        image.save()
        return comment._id
