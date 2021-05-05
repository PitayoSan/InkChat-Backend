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

	def __init_storage(self):
		try:
			return storage.bucket(os.environ['FS_BUCKET'])
		except KeyError:
			print("FS_BUCKET not found in system")
			print("Storage could not be initialized")

	# Utils
	def __get_user_doc(self, uid):
		return self.__db.collection('users').document(uid)

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

	# Public Methods
	# Users
	def create_user(self, username, email, pw, encoded_pp=None):
		try:
			user_record = auth.create_user(email=email, password=pw)
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
		if sender_doc.get().to_dict() is None: return response(404, "sender not found")

		user_doc = self.__get_user_doc(dest)
		if user_doc.get().to_dict() is None: return response(404, "dest not found")        

		friends = user_doc.get().to_dict()['friends']
		if sender in friends:
			return response(
				403,
				"sender is already friends with dest or there is already a pending friend request between them"
			)
		
		user = user_doc.get().to_dict()
		friends[sender] = {
			'username': user['username'],
			'pp': user['pp'],
			'is_friends': False,
		}
		user_doc.set({'friends': friends}, merge=True)
		return response(201, dest)

	def accept_friend_request(self, sender, dest):
		sender_doc = self.__get_user_doc(sender)
		if sender_doc.get().to_dict() is None: return response(404, "sender not found")
		
		dest_doc = self.__get_user_doc(dest)
		if dest_doc.get().to_dict() is None: return response(404, "dest not found")
	
		dest_friends = dest_doc.get().to_dict()['friends']
		if sender not in dest_friends or dest_friends[sender] == True:
			return response(403, "there is no pending friend request between sender and dest")
		
		sender_friends = sender_doc.get().to_dict()['friends']
		dest_friends[sender] = True
		dest_doc.set({'friends': dest_friends}, merge=True)
		sender_friends[dest] = True
		sender_doc.set({'friends': sender_friends}, merge=True)
		return response(201, sender)

	def delete_friend_or_friend_request(self, uid, friend):
		user_doc = self.__get_user_doc(uid)
		if user_doc.get().to_dict() is None: return response(404, "user not found")

		friend_doc = self.__get_user_doc(friend)
		user_friends = user_doc.get().to_dict()['friends']
		if friend not in user_friends:
			return response(
				403,
				"friend isn't a friend of user or there is no pending friend request between them"
			)
		
		friend_friends = friend_doc.get().to_dict()['friends']
		user_friends.pop(friend)
		temp = user_doc.get().to_dict()
		temp['friends'] = user_friends
		user_doc.set(temp)
		
		if uid in friend_friends:
			friend_friends.pop(uid)
			temp = friend_doc.get().to_dict()
			temp['friends'] = friend_friends
			friend_doc.set(temp)
		return response(200, friend)
