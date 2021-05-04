import pytest
import json

from flaskr import app


GET_USER_PARAMS = [
    # Existent user
    (
        {"username": "test_user"},
        200,
        {
            "email": "test_mail",
            "friends": {}, # TODO
            "pp": "", # TODO
            "username": "test_user"
        }
    ),

    # Non existent user
    (
        {"username": "non_existent_user"},
        404,
        "user not found"
    ),

    # No request body
    ({}, 400, "username: username of requested user")
]

CREATE_USER_PARAMS = [
    # Success with path
    (
        {
            "username": "test_user",
            "email": "test_mail",
            "path": "" # TODO
        },
        201,
        {
            "email": "test_mail",
            "friends": {},
            "pp": "", # TODO
            "username": "test_user"
        }
    ),

    # Success without path
    (
        {
            "username": "test_user",
            "email": "test_mail"
        },
        201,
        {
            "email": "test_mail",
            "friends": {},
            "pp": "",
            "username": "test_user"
        }
    ),

    # No username in body
    (
        {
            "email": "test_mail"
        },
        400,
        "username: username of user being created"
		"email: email of user being created"
		"(optional) path: path of the file to upload"
    ),

    # No email in body
    (
        {
            "username": "test_user",
        },
        400,
        "username: username of user being created"
		"email: email of user being created"
		"(optional) path: path of the file to upload"
    ),

    # No request body
    (
        {},
        400,
        "username: username of user being created"
		"email: email of user being created"
		"(optional) path: path of the file to upload"
    )
]

GET_USER_PP_PARAMS = [
    # Existent user
    (
        {"username": "test_user"},
        200,
        {
            "pp": "" # TODO
        }
    ),

    # Non existent user
    (
        {"username": "non_existent_user"},
        404,
        "user not found"
    ),

    # No request body
    ({}, 400, "username: username of owner of the pic")
]

UPDATE_USER_PP_PARAMS = [
    # Existent user
    (
        {
            "username": "test_user",
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
            "username": "test_user"
        },
        400,
        "username: username of owner of the pic"
        "path: path to the file"
    )

    # No username in body # TODO

    # No request body # TODO
]

@pytest.mark.parametrize(
    "username, status_code, data",
    GET_USER_PARAMS
)
def test_get_user(client, username, status_code, data):
    response = client.get('/users', query_string=username)
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
    "username, status_code, data",
    GET_USER_PP_PARAMS
)
def test_get_user_pp(client, username, status_code, data):
    response = client.get('/users/pp', query_string=username)
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
