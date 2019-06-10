import os
def test_post_image_success(client, utility):

    url = '/post_image'

    img_name = 'cheese.jpg'

    data = {'file': open(img_name, 'rb')}

    response = client.post(url, buffered=True,
                           content_type='multipart/form-data',
                           data=data, headers=utility.mock_token())
    
    assert os.path.exists('/app/images/'+img_name) == True
    assert response.status_code == 201