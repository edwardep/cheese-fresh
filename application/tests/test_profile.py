def test_get_profile_success(client, utility):
    # create 2 users
    utility.mock_user('user')
    utility.mock_user('john')

    # 'user' visits john's profile
    url = '/public_profile?user=john'
    response = client.get(url, headers=utility.mock_token())

    assert response.status_code == 200
    assert response.json['username'] == 'john'

    # not following John yet ~UI: render Follow btn
    assert response.json['is_stranger'] == True

# expecting 404
# def test_get_profile_not_found(client, utility):

#     utility.mock_user('user')
#     url = '/public_profile?user=user1'
#     response = client.get(url, headers=utility.mock_token())

#     assert response.status_code == 404
