import pytest
import json

from flaskr import app

TEST_UID = '0KEYuXyOxcUjNSESd4RHeAOi3BP2'
TEST1_UID = 'DM2wPOAS0Rerk58bNn5kxs81K452'
TEST2_UID = 'rMP0MM14zmTdR7T0E9f8m2hJDfG3'

GET_ALL_FRIENDS_PARAMS = [
	# Uses user 0
	# Existent user
	(
		{"uid": TEST_UID},
		200,
		{
			"friends": {
				TEST1_UID: False,
				TEST2_UID: True
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
	# Uses users 1-2
	# Existent user3 to Existent user4
	(
		{"sender": TEST1_UID, "dest": TEST2_UID},
		201,
		TEST2_UID
	),

	# Same user in sender and dest
	(
		{"sender": TEST1_UID, "dest": TEST1_UID},
		400,
		"sender and dest can't be the same"
	),

	# No sender in body
	(
		{"dest": TEST1_UID},
		400,
		"sender: user sending friend request"
		"dest: user the friend request is being sent to"
	),

	# No dest in body
	(
		{"sender": TEST1_UID},
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
	response = client.post('/friends', json=body)
	json_data = response.get_json()

	assert response.status_code == status_code
	assert json_data["data"] == data
