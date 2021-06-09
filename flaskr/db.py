import re
import os
import base64
import firebase_admin
from uuid import uuid4

from mimetypes import guess_extension
from flaskr.utils.responses import response
from firebase_admin import credentials, firestore, storage, auth


class FireDB():
	# Inits
	def __init__(self):
		self.__cred = credentials.Certificate('./key.json')
		firebase_admin.initialize_app(self.__cred)
		self.__db = firestore.client()
		self.__bucket = self.__init_storage()
		self.auth = auth

	def __init_storage(self):
		try:
			return storage.bucket(os.environ['FS_BUCKET'])
		except KeyError:
			print("FS_BUCKET not found in system")
			print("Storage could not be initialized")

	# Utils
	def __get_user_doc(self, uid):
		return self.__db.collection('users').document(uid)

	def __get_user_doc_where_username(self, username):
		return self.__db.collection('users').where('username', '==', username)

	def __is_user_unique(self, username):
		user_doc = self.__get_user_doc_where_username(username)
		users = user_doc.get()
		if len(users) == 0:
			return True
		return False

	def __get_user_uid(self, username):
		user_doc = self.__get_user_doc_where_username(username)
		users = user_doc.get()
		if len(users) == 0:
			return None
		if len(users) > 1:
			return None
		return users[0].to_dict()['uid']

	def __upload_user_pp(self, uid, encoded_pp):
		allowed_extensions = ['image/png', 'image/jpg', 'image/jpeg', 'image/gif']
		split_pp = encoded_pp.split(',')
		pp_type = re.split(':|;', split_pp[0])[1]

		if pp_type not in allowed_extensions:
			raise TypeError(f"{pp_type} is not an allowed type")

		decoded_pp = base64.b64decode(split_pp[1])

		pp_name = f'{uid}.jpg'
		blob = self.__bucket.blob(f'users/pp/{pp_name}')

		new_token = uuid4()
		metadata  = {"firebaseStorageDownloadTokens": new_token}
		blob.metadata = metadata

		blob.upload_from_string(decoded_pp, content_type=pp_type)
		blob.make_public()
		return blob.public_url

	def __get_group_list(self):
		groups = []
		groups_docs = self.__db.collection('groups').stream()
		for doc in groups_docs:
			groups.append(doc.to_dict()['name'])
		return groups

	# Public Methods
	# Users
	def create_user(self, username, email, pw, encoded_pp=None):
		if not self.__is_user_unique(username):
			return response(403, "username already exists")

		try:
			user_record = self.auth.create_user(email=email, password=pw)
		except firebase_admin._auth_utils.EmailAlreadyExistsError:
			return response(403, "user already exists")

		uid = user_record.uid

		user = {
			'uid': uid,
			'username': username,
			'friends': {},
			'pp': self.__upload_user_pp(uid, encoded_pp) if encoded_pp else ''
		}

		user_doc = self.__get_user_doc(uid)
		user_doc.set(user)
		return response(201, user)

	def get_user(self, uid):
		user_doc = self.__get_user_doc(uid)
		user = user_doc.get().to_dict()
		if user: return response(200, user)
		return response(404, "user not found")

	def get_user_pp(self, uid):
		user_doc = self.__get_user_doc(uid)
		pp_link = user_doc.get(['pp']).to_dict()
		if pp_link: return response(200, pp_link)
		return response(404, "user not found")

	def update_user_pp(self, uid, encoded_pp):
		try:
			pp_link = self.__upload_user_pp(uid, encoded_pp)
		except TypeError as te:
			return response(403, str(te))
		user_doc = self.__get_user_doc(uid)

		pp = {
			'pp': pp_link
		}

		user_doc.update(pp)
		return response(201, pp)

	# Friends
	def get_all_friends(self, uid):
		user_doc = self.__get_user_doc(uid)
		friends = user_doc.get(['friends']).to_dict()
		if friends: return response(200, friends)
		return response(404, "user not found")

	def send_friend_request(self, sender, dest):
		sender_doc = self.__get_user_doc(sender)
		sender_dict = sender_doc.get().to_dict()
		if sender_dict is None: return response(404, "sender not found")

		dest_uid = self.__get_user_uid(dest)
		if dest_uid is None: return response(404, "dest not found")

		dest_doc = self.__get_user_doc(dest_uid)
		dest_dict = dest_doc.get().to_dict()
		if dest_dict is None: return response(404, "dest not found")

		dest_friends = dest_dict['friends']
		if sender in dest_friends:
			return response(
				403,
				"sender is already friends with dest or there is already a pending friend request between them"
			)

		dest_friends[sender] = {
			'username': sender_dict['username'],
			'pp': sender_dict['pp'],
			'is_friends': False,
		}
		dest_doc.set({'friends': dest_friends}, merge=True)
		return response(201, dest_uid)

	def accept_friend_request(self, sender, dest):
		sender_doc = self.__get_user_doc(sender)
		sender_dict = sender_doc.get().to_dict()
		if sender_dict is None: return response(404, "sender not found")

		dest_doc = self.__get_user_doc(dest)
		dest_dict = dest_doc.get().to_dict()
		if dest_dict is None: return response(404, "dest not found")

		dest_friends = dest_dict['friends']
		if sender not in dest_friends or dest_friends[sender] == True:
			return response(403, "there is no pending friend request between sender and dest")
		sender_friends = sender_dict['friends']

		channel = 'chan_' + sender_dict['username'] + '_' + dest_dict['username']

		temp = dest_friends[sender]
		temp['is_friends'] = True
		temp['channel'] = channel
		dest_friends[sender] = temp
		dest_doc.set({'friends': dest_friends}, merge=True)


		sender_friends[dest] = {
			'username': dest_dict['username'],
			'pp': dest_dict['pp'],
			'is_friends': True,
			'channel': channel,
		}
		sender_doc.set({'friends': sender_friends}, merge=True)
		return response(201, sender)

	def delete_friend_or_friend_request(self, uid, friend):
		user_doc = self.__get_user_doc(uid)
		user_dict = user_doc.get().to_dict()
		if user_dict is None: return response(404, "user not found")

		friend_doc = self.__get_user_doc(friend)
		friend_dict = friend_doc.get().to_dict()
		user_friends = user_dict['friends']
		if friend not in user_friends:
			return response(
				403,
				"friend isn't a friend of user or there is no pending friend request between them"
			)

		friend_friends = friend_dict['friends']
		user_friends.pop(friend)
		temp = user_dict
		temp['friends'] = user_friends
		user_doc.set(temp)

		if uid in friend_friends:
			friend_friends.pop(uid)
			temp = friend_dict
			temp['friends'] = friend_friends
			friend_doc.set(temp)
		return response(200, friend)

	# Groups
	def get_all_groups(self):
		return response(200, self.__get_group_list())

	def create_group(self, name):
		if name in self.__get_group_list():
			return response(403, "group already exists")

		group = {
			'name': name,
			'msg': [],
		}

		doc_ref = self.__db.collection('groups').document(name)
		doc_ref.set(group)
		return response(201, group)

	def get_group(self, name):
		group_ref = self.__db.collection('groups').document(name)
		group = group_ref.get().to_dict()
		if group: return response(200, group)
		return response(404, "group not found")

	def send_message(self, name, msg, uid, username, time, pp):
		group_ref = self.__db.collection('groups').document(name)
		group = group_ref.get().to_dict()
		if group:
			message = {
				'data': msg,
				'uid': uid,
				'username': username,
				'time': time,
				'pp': pp
			}

			messages = group['msg']
			messages.append(message)

			group_ref.set({'msg': messages}, merge=True)
			return response(200, message)
		return response(404, "group not found")
