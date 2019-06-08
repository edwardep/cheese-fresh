from io import BytesIO
import pytest
import os


def test_post_image_success(client, utility):
    pytest.skip('not_checked')
    utility.mock_user('user')
    utility.mock_gallery('gallery')

    data = {'file': (BytesIO(b'IMAGE DATA'), 'tokio.jpg')}

    response = client.post('/add_image?title=gallery', buffered=True,
                           content_type='multipart/form-data',
                           data=data, headers=utility.mock_token())
    assert response.status_code == 201
    assert response.json['owner'] == 'user'


def test_post_image_gallery_not_found(client, utility):
    pytest.skip('not_checked')
    utility.mock_user('user')
    # Gallery is missing

    response = client.post('/add_image?title=', buffered=True,
                           content_type='multipart/form-data',
                           data={}, headers=utility.mock_token())
    assert response.status_code == 404


def test_post_image_bad_type(client, utility):
    pytest.skip('not_checked')
    utility.mock_user('user')
    utility.mock_gallery('gallery')

    data = {'txt': (BytesIO(b'IMAGE DATA'), 'tokio.jpg')}
    response = client.post('/add_image?title=gallery', buffered=True,
                           content_type='multipart/form-data',
                           data=data, headers=utility.mock_token())
    assert response.status_code == 400


def test_post_image_bad_filename(client, utility):
    pytest.skip('not_checked')
    utility.mock_user('user')
    utility.mock_gallery('gallery')

    data = {'file': ''}
    response = client.post('/add_image?title=gallery', buffered=True,
                           content_type='multipart/form-data',
                           data=data, headers=utility.mock_token())
    assert response.status_code == 400


def test_post_image_bad_extension(client, utility):
    pytest.skip('not_checked')
    utility.mock_user('user')
    utility.mock_gallery('gallery')

    data = {'file': (BytesIO(b'IMAGE DATA'), 'tokio.pdf')}
    response = client.post('/add_image?title=gallery', buffered=True,
                           content_type='multipart/form-data',
                           data=data, headers=utility.mock_token())
    assert response.status_code == 400
