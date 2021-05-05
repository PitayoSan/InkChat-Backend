import pytest
import json

from flaskr import app

TEST_UID = '0KEYuXyOxcUjNSESd4RHeAOi3BP2'
TEST1_UID = 'DM2wPOAS0Rerk58bNn5kxs81K452'
TEST2_UID = 'rMP0MM14zmTdR7T0E9f8m2hJDfG3'
NON_UID = 'vue_boss'
NON_UID2 = 'draiben'

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
	# Existent user1 to Existent user2
	(
		{"sender": TEST1_UID, "dest": TEST2_UID},
		201,
		TEST2_UID
	),

	# Existent user2 to Existent user1
	(
		{"sender": TEST2_UID, "dest": TEST1_UID},
		201,
		TEST1_UID
	),

	# Existent user1 to Existent user2 (existent FR)
	(
		{"sender": TEST1_UID, "dest": TEST2_UID},
		403,
		"sender is already friends with dest or there is already a pending friend request between them"
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

	# Non existent user69 to existent user2
	(
		{"sender": NON_UID, "dest": TEST2_UID},
		404,
		"sender not found"
	),

	# Existent user2 to non existent user69
	(
		{"sender": TEST2_UID, "dest": NON_UID},
		404,
		"dest not found"
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
	)
]

ACCEPT_FRIEND_REQUEST_PARAMS = [
	# Uses users 1-2

	# Existent user1 to existent user2
	(
		{"sender": TEST1_UID, "dest": TEST2_UID},
		201,
		TEST1_UID
	),

	# Existent user1 to existent user2 (non existent FR)
	(
		{"sender": TEST1_UID, "dest": TEST2_UID},
		403,
		"there is no pending friend request between sender and dest"
	),

	# Non existent user69 to existent user2 (existent FR)
	(
		{"sender": NON_UID, "dest": TEST2_UID},
		404,
		"sender not found"
	),

	# Existent user1 to non existent user69 (existent FR)
	(
		{"sender": TEST1_UID, "dest": NON_UID},
		404,
		"dest not found"
	),

	# Same user in sender and dest
	(
		{"sender": TEST1_UID, "dest": TEST1_UID},
		400,
		"sender and dest can't be the same"
	),

	# No sender in body
	(
		{"dest": TEST2_UID},
		400,
		"sender: user that sent the friend request"
		"dest: user that is accepting the friend request"
	),

	# No dest in body
	(
		{"sender": TEST2_UID},
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
	# Uses users 1-2

	# Existent user1, existen FR
	(
		{"uid": TEST1_UID, "friend": TEST2_UID},
		200,
		TEST2_UID
	),

	# Existent user1, non existen FR
	(
		{"uid": TEST1_UID, "friend": NON_UID},
		403,
		"friend isn't a friend of user or there is no pending friend request between them"
	),

	# Non existent user, non existen FR
	(
		{"uid": NON_UID2, "friend": NON_UID},
		404,
		"user not found"
	),

	# Same uid and friend
	(
		{"uid": NON_UID, "friend": NON_UID},
		400,
		"uid and friend can't be the same"
	),

	# No uid in body
	(
		{"friend": NON_UID},
		400,
		"uid: user that's deleting a friend"
		"friend: user that's being deleted"
	),

	# No friend in body
	(
		{"uid": NON_UID},
		400,
		"uid: user that's deleting a friend"
		"friend: user that's being deleted"
	),

	# No request body
	(
		{},
		400,
		"uid: user that's deleting a friend"
		"friend: user that's being deleted"
	),
]

@pytest.mark.parametrize(
	"uid, status_code, data",
	GET_ALL_FRIENDS_PARAMS
)
def test_get_all_friends(client, uid, status_code, data):
	response = client.get('/friends', query_string=uid)
	json_data = response.get_json()

	assert response.status_code == status_code and json_data["data"] == data


@pytest.mark.parametrize(
	"body, status_code, data",
	SEND_FRIEND_REQUEST_PARAMS
)
def test_send_friend_request(client, body, status_code, data):
	response = client.post('/friends', json=body)
	json_data = response.get_json()

	assert response.status_code == status_code and json_data["data"] == data


@pytest.mark.parametrize(
	"body, status_code, data",
	ACCEPT_FRIEND_REQUEST_PARAMS
)
def test_accept_friend_request(client, body, status_code, data):
	response = client.put('/friends', json=body)
	json_data = response.get_json()

	assert response.status_code == status_code and json_data["data"] == data


@pytest.mark.parametrize(
	"body, status_code, data",
	DELETE_FRIEND_REQUEST_PARAMS
)
def test_DELETE_friend_request(client, body, status_code, data):
	response = client.delete('/friends', query_string=body)
	json_data = response.get_json()

	assert response.status_code == status_code and json_data["data"] == data
