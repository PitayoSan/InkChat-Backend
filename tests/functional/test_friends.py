import pytest
import json

from flaskr import app


GET_ALL_FRIENDS_PARAMS = [
    # Uses user 1

    # Existent user
    (
        {"username": "test_friends_user_1"},
        200,
        {
            "friends": {
                "test_friends_user_10": False,
                "test_friends_user_11": False,
                "test_friends_user_12": True
            }
        }
    ),

    # Non existent user
    (
        {"username": "non_existent_user"},
        404,
        "user not found"
    ),

    # No request body
    ({}, 400, "username: user to get all friends from")
]

SEND_FRIEND_REQUEST_PARAMS = [
    # Uses users 2-3

    # Existent user2 to existent user3
    (
        {"sender": "test_friends_user_2", "dest": "test_friends_user_3"},
        201,
        "test_friends_user_3"
    ),

    # Existent user3 to existent user2
    (
        {"sender": "test_friends_user_3", "dest": "test_friends_user_2"},
        201,
        "test_friends_user_2"
    ),

    # Existent user2 to existent user3 (existent FR)
    (
        {"sender": "test_friends_user_2", "dest": "test_friends_user_3"},
        400,
        "sender is already friends with dest or there is already a pending friend request between them"
    ),

    # Non existent user69 to non existent user2 (existent FR)
    (
        {"sender": "test_friends_user_69", "dest": "test_friends_user_2"},
        404,
        "sender not found"
    ),

    # Existent user2 to non existent user69 (existent FR)
    (
        {"sender": "test_friends_user_2", "dest": "test_friends_user_69"},
        404,
        "dest not found"
    ),

    # Same user in sender and dest
    (
        {"sender": "test_friends_user_2", "dest": "test_friends_user_2"},
        400,
        "sender and dest can't be the same"
    ),

    # No sender in body
    (
        {"dest": "test_friends_user_2"},
        400,
        "sender: user sending friend request"
		"dest: user the friend request is being sent to"
    ),

    # No dest in body
    (
        {"sender": "test_friends_user_2"},
        400,
        "sender: user sending friend request"
		"dest: user the friend request is being sent to"
    ),

    # No request body
    (
        {},
        400,
        "sender: user sending friend request"
		"dest: user the friend request is being sent to"
    )
]

ACCEPT_FRIEND_REQUEST_PARAMS = [
    # Uses users 2-3

    # Existent user2 to existent user3
    (
        {"sender": "test_friends_user_2", "dest": "test_friends_user_3"},
        201,
        "test_friends_user_2"
    ),

    # Existent user2 to existent user3 (non existent FR)
    (
        {"sender": "test_friends_user_2", "dest": "test_friends_user_3"},
        400,
        "there is no pending friend request between sender and dest"
    ),

    # Non existent user69 to non existent user2 (existent FR) # TODO
    (
        {"sender": "test_friends_user_69", "dest": "test_friends_user_2"},
        404,
        "sender not found"
    ),

    # Existent user2 to non existent user69 (existent FR)
    (
        {"sender": "test_friends_user_2", "dest": "test_friends_user_69"},
        404,
        "dest not found"
    ),

    # Same user in sender and dest
    (
        {"sender": "test_friends_user_2", "dest": "test_friends_user_2"},
        400,
        "sender and dest can't be the same"
    ),

    # No sender in body
    (
        {"dest": "test_friends_user_2"},
        400,
        "sender: user that sent the friend request"
		"dest: user that is accepting the friend request"
    ),

    # No dest in body
    (
        {"sender": "test_friends_user_2"},
        400,
        "sender: user that sent the friend request"
		"dest: user that is accepting the friend request"
    ),

    # No request body
    (
        {},
        400,
        "sender: user that sent the friend request"
		"dest: user that is accepting the friend request"
    )
]

DELETE_FRIEND_REQUEST_PARAMS = [
    # Uses users 2-3

    # Existent user2, existen FR
    (
        {"username": "test_friends_user_2", "friend": "test_friends_user_3"},
        200,
        "test_friends_user_3"
    ),

    # Existent user, non existen FR
    (
        {"username": "test_friends_user_2", "friend": "test_friends_user_69"},
        400,
        "friend isn't a friend of user or there is no pending friend request between them"
    ),

    # Non existent user, non existen FR
    (
        {"username": "test_friends_user_68", "friend": "test_friends_user_69"},
        404,
        "user not found"
    ),

    # Same username and friend
    (
        {"username": "test_friends_user_69", "friend": "test_friends_user_69"},
        400,
        "username and friend can't be the same"
    ),

    # No username in body
    (
        {"friend": "test_friends_user_69"},
        400,
        "username: user that's deleting a friend"
		"friend: user that's being deleted"
    ),

    # No friend in body
    (
        {"username": "test_friends_user_69"},
        400,
        "username: user that's deleting a friend"
		"friend: user that's being deleted"
    ),

    # No request body
    (
        {},
        400,
        "username: user that's deleting a friend"
		"friend: user that's being deleted"
    ),
]

@pytest.mark.parametrize(
    "username, status_code, data",
    GET_ALL_FRIENDS_PARAMS
)
def test_get_all_friends(client, username, status_code, data):
    response = client.get('/friends', query_string=username)
    json_data = response.get_json()

    assert response.status_code == status_code
    assert json_data["data"] == data


@pytest.mark.parametrize(
    "body, status_code, data",
    SEND_FRIEND_REQUEST_PARAMS
)
def test_send_friend_request(client, body, status_code, data):
    response = client.post('/friends', json=json.dumps(body))
    json_data = response.get_json()

    assert response.status_code == status_code
    assert json_data["data"] == data


@pytest.mark.parametrize(
    "body, status_code, data",
    ACCEPT_FRIEND_REQUEST_PARAMS
)
def test_accept_friend_request(client, body, status_code, data):
    response = client.put('/friends', json=json.dumps(body))
    json_data = response.get_json()

    assert response.status_code == status_code
    assert json_data["data"] == data


@pytest.mark.parametrize(
    "body, status_code, data",
    DELETE_FRIEND_REQUEST_PARAMS
)
def test_DELETE_friend_request(client, body, status_code, data):
    response = client.delete('/friends', query_string=body)
    json_data = response.get_json()

    assert response.status_code == status_code
    assert json_data["data"] == data
