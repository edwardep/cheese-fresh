from auth import app
import pytest
from mongoengine import connect


@pytest.fixture
def client():
    client = app.test_client()
    db = connect('cheese-test')
    db.drop_database('cheese-test')
    yield client
    db.drop_database('cheese-test')


@pytest.fixture
def utility():
    return Utility


class Utility:
    @staticmethod
    def register_user(client, username, password):
        url = '/register'
        data = {
            'username': username,
            'password': password,
            'email': username + '@email.com'
        }
        return client.post(url, json=data)

    @staticmethod
    def login_user(client, username, password):
        url = '/login'
        data = {'username': username, 'password': password}
        return client.post(url, json=data)
