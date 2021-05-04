import pytest
import json

from flaskr import app


GET_ALL_FRIENDS_PARAMS = [
	# Uses user 1
	# Existent user
	(
		{"uid": "test_friends_user_1"},
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
		{"uid": "non_existent_user"},
		404,
		"user not found"
	),

	# No request body
	({}, 400, "uid: user to get all friends from")
]

SEND_FRIEND_REQUEST_PARAMS = [
	# Uses users 2-3
	# Existent user3 to Existent user4
	(
		{"sender": "test_friends_user_2", "dest": "test_friends_user_3"},
		201,
		"test_friends_user_3"
	),

	# Existent user4 to Existent user3
	(
		{"sender": "test_friends_user_3", "dest": "test_friends_user_2"},
		201,
		"test_friends_user_2"
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
	),
]

@pytest.mark.parametrize(
	"uid, status_code, data",
	GET_ALL_FRIENDS_PARAMS
)
def test_get_all_friends(client, uid, status_code, data):
	response = client.get('/friends', query_string=uid)
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
