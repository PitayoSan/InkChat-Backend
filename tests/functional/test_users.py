import pytest
import json

from flaskr import app

TEST_UID = '0KEYuXyOxcUjNSESd4RHeAOi3BP2'
TEST1_UID = 'DM2wPOAS0Rerk58bNn5kxs81K452'
TEST2_UID = 'rMP0MM14zmTdR7T0E9f8m2hJDfG3'

GET_USER_PARAMS = [
	# Existent user
	(
		{"uid": TEST_UID},
		200,
		{
			"uid": TEST_UID,
			"username": "test_username",
			"friends": {
				TEST1_UID: False,
				TEST2_UID: True
			},
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
			"username": "test_username",
			"email": "test@email.com",
			"pw": "123456",
			"path": "" # TODO
		},
		201,
		{
			"uid": TEST_UID,
			"username": "test_username",
			"friends": {},
			"pp": "", # TODO
		}
	),

	# Success without path
	(
		{
			"username": "test_username",
			"email": "test@email.com",
			"pw": "123456",
		},
		201,
		{
			"uid": TEST_UID,
			"username": "test_username",
			"friends": {},
			"pp": "", # TODO
		}
	),

	# No email in body
	(
		{
			"username": "test_user"
		},
		400,
		"username: username of user being created"
		"email: email of user being created"
		"pw: password of user being created"
		"(optional) path: path of the file to upload"
	),

	# No username in body
	(
		{
			"email": "test_user@mail.com",
		},
		400,
		"username: username of user being created"
		"email: email of user being created"
		"pw: password of user being created"
		"(optional) path: path of the file to upload"
	),

	# No request body
	(
		{},
		400,
		"username: username of user being created"
		"email: email of user being created"
		"pw: password of user being created"
		"(optional) path: path of the file to upload"
	)
]

GET_USER_PP_PARAMS = [
	# Existent user
	(
		{"uid": TEST_UID},
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
			"uid": TEST_UID,
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
			"uid": TEST_UID
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
	response = client.post('/users', json=body)
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
	response = client.post('/users/pp', json=body)
	json_data = response.get_json()

	assert response.status_code == status_code
	assert json_data["data"] == data
