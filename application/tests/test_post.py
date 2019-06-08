from io import BytesIO
import pytest
import os

@pytest.mark.xfail
def test_post_follow_success(client, utility):
    pass

@pytest.mark.xfail
def test_post_follow_unacceptable(client, utility):
    pass

@pytest.mark.xfail
def test_post_follow_not_found(client, utility):
    pass

@pytest.mark.xfail
def test_post_gallery_success(client, utility):
    utility.mock_user('user')

    url = '/add_gallery'
    data = {'gallery_title': 'gallery'}
    response = client.post(url, data, headers=utility.mock_token())

    assert response.status_code == 201


def test_post_image_success(client, utility):
    utility.mock_user('user')
    utility.mock_gallery('gallery')

    data = {'file': (BytesIO(b'IMAGE DATA'), 'tokio.jpg')}

    response = client.post('/add_image?gallery_title=gallery', buffered=True,
                           content_type='multipart/form-data',
                           data=data, headers=utility.mock_token())
    assert response.status_code == 201


def test_post_image_gallery_not_found(client, utility):
    utility.mock_user('user')
    # Gallery is missing

    response = client.post('/add_image?gallery_title=', buffered=True,
                           content_type='multipart/form-data',
                           data={}, headers=utility.mock_token())
    assert response.status_code == 404


def test_post_image_bad_type(client, utility):
    utility.mock_user('user')
    utility.mock_gallery('gallery')

    data = {'txt': (BytesIO(b'IMAGE DATA'), 'tokio.jpg')}
    response = client.post('/add_image?gallery_title=gallery', buffered=True,
                           content_type='multipart/form-data',
                           data=data, headers=utility.mock_token())
    assert response.status_code == 400


def test_post_image_bad_filename(client, utility):
    utility.mock_user('user')
    utility.mock_gallery('gallery')

    data = {'file': ''}
    response = client.post('/add_image?gallery_title=gallery', buffered=True,
                           content_type='multipart/form-data',
                           data=data, headers=utility.mock_token())
    assert response.status_code == 400


def test_post_image_bad_extension(client, utility):
    utility.mock_user('user')
    utility.mock_gallery('gallery')

    data = {'file': (BytesIO(b'IMAGE DATA'), 'tokio.pdf')}
    response = client.post('/add_image?gallery_title=gallery', buffered=True,
                           content_type='multipart/form-data',
                           data=data, headers=utility.mock_token())
    assert response.status_code == 400

@pytest.mark.xfail
def test_post_comment_success(client, utility):
    pass

@pytest.mark.xfail
def test_post_comment_not_found(client, utility):
    pass

@pytest.mark.xfail
def test_post_comment_forbidden(client, utility):
    pass
