import pytest
import json

from flaskr import app


GET_USER_PARAMS = [
    # Existent user
    (
        {"uid": "test_user"},
        200,
        {
            "uid": "test_user",
            "username": "test_user",
            "friends": {}, # TODO
            "pp": "", # TODO
        }
    ),

    # Non existent user
    (
        {"uid": "non_existent_user"},
        404,
        "user not found"
    ),

    # No request body
    ({}, 400, "uid: uid of requested user")
]

CREATE_USER_PARAMS = [
    # Success with path
    (
        {
            "uid": "test_user",
            "username": "test_user",
            "path": "" # TODO
        },
        201,
        {
            "uid": "test_user",
            "username": "test_user",
            "friends": {},
            "pp": "", # TODO
        }
    ),

    # Success without path
    (
        {
            "uid": "test_user",
            "username": "test_user",
        },
        201,
        {
            "uid": "test_user",
            "username": "test_user",
            "friends": {},
            "pp": "", # TODO
        }
    ),

    # No uid in body
    (
        {
            "username": "test_user"
        },
        400,
        "uid: uid of user being created"
        "username: username of user being created"
		"(optional) path: path of the file to upload"
    ),

    # No username in body
    (
        {
            "uid": "test_user",
        },
        400,
        "uid: uid of user being created"
        "username: username of user being created"
		"(optional) path: path of the file to upload"
    ),

    # No request body
    (
        {},
        400,
        "uid: uid of user being created"
        "username: username of user being created"
		"(optional) path: path of the file to upload"
    )
]

GET_USER_PP_PARAMS = [
    # Existent user
    (
        {"uid": "test_user"},
        200,
        {
            "pp": "" # TODO
        }
    ),

    # Non existent user
    (
        {"uid": "non_existent_user"},
        404,
        "user not found"
    ),

    # No request body
    ({}, 400, "uid: uid of owner of the pic")
]

UPDATE_USER_PP_PARAMS = [
    # Existent user
    (
        {
            "uid": "test_user",
            "path": "" # TODO
        },
        201,
        {
            "pp": "" # TODO
        }
    ),

    # No path in body
    (
        {
            "uid": "test_user"
        },
        400,
        "uid: uid of owner of the pic"
        "path: path to the file"
    )

    # No uid in body # TODO

    # No request body # TODO
]

@pytest.mark.parametrize(
    "uid, status_code, data",
    GET_USER_PARAMS
)
def test_get_user(client, uid, status_code, data):
    response = client.get('/users', query_string=uid)
    json_data = response.get_json()

    assert response.status_code == status_code
    assert json_data["data"] == data


@pytest.mark.parametrize(
    "body, status_code, data",
    CREATE_USER_PARAMS
)
def test_create_user(client, body, status_code, data):
    response = client.post('/users', json=json.dumps(body))
    json_data = response.get_json()

    assert response.status_code == status_code
    assert json_data["data"] == data


@pytest.mark.parametrize(
    "uid, status_code, data",
    GET_USER_PP_PARAMS
)
def test_get_user_pp(client, uid, status_code, data):
    response = client.get('/users/pp', query_string=uid)
    json_data = response.get_json()

    assert response.status_code == status_code
    assert json_data["data"] == data


@pytest.mark.parametrize(
    "body, status_code, data",
    UPDATE_USER_PP_PARAMS
)
def test_update_user_pp(client, body, status_code, data):
    response = client.post('/users/pp', json=json.dumps(body))
    json_data = response.get_json()

    assert response.status_code == status_code
    assert json_data["data"] == data
