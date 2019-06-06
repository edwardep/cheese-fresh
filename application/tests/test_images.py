from io import BytesIO
import pytest
import os


# def test_get_images_success(client, utility):
#     pass #200

# def test_get_images_not_found(client, utility):
#     pass  # 404


def test_post_image_success(client, utility):
    utility.mock_user('user')
    utility.mock_gallery('gallery')

    data = {'file': (BytesIO(b'IMAGE DATA'), 'tokio.jpg')}

    response = client.post('/add_image?title=gallery', buffered=True,
                           content_type='multipart/form-data',
                           data=data, headers=utility.mock_token())
    assert response.status_code == 201
    assert response.json['owner'] == 'user'


def test_post_image_gallery_not_found(client, utility):
    utility.mock_user('user')
    # Gallery is missing

    response = client.post('/add_image?title=', buffered=True,
                           content_type='multipart/form-data',
                           data={}, headers=utility.mock_token())
    assert response.status_code == 404


def test_post_image_bad_type(client, utility):
    utility.mock_user('user')
    utility.mock_gallery('gallery')

    data = {'txt': (BytesIO(b'IMAGE DATA'), 'tokio.jpg')}
    response = client.post('/add_image?title=gallery', buffered=True,
                           content_type='multipart/form-data',
                           data=data, headers=utility.mock_token())
    assert response.status_code == 400


def test_post_image_bad_filename(client, utility):
    utility.mock_user('user')
    utility.mock_gallery('gallery')

    data = {'file': ''}
    response = client.post('/add_image?title=gallery', buffered=True,
                           content_type='multipart/form-data',
                           data=data, headers=utility.mock_token())
    assert response.status_code == 400


def test_post_image_bad_extension(client, utility):
    utility.mock_user('user')
    utility.mock_gallery('gallery')

    data = {'file': (BytesIO(b'IMAGE DATA'), 'tokio.pdf')}
    response = client.post('/add_image?title=gallery', buffered=True,
                           content_type='multipart/form-data',
                           data=data, headers=utility.mock_token())
    assert response.status_code == 400
