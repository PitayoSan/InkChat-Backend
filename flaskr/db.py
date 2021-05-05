import os
import firebase_admin

from flaskr.utils.responses import response
from firebase_admin import credentials, firestore, storage


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
    def __get_user_doc(self, username):
        return self.__db.collection('users').document(username)

    def __upload_user_pp(self, username, path):
        _, file_extension = os.path.splitext(path)
        pp_name = f"{username}{file_extension}"
        blob = self.__bucket.blob(f"users/pp/{pp_name}")

        file_dir = os.path.dirname(path)
        os.chdir('/mnt/c/Games')

        file_name = os.path.basename(path)
        with open(file_name, 'rb') as file:
            blob.upload_from_file(file)

        return blob.public_url

    # Public Methods
    # Users
    def create_user(self, username, email, pp_path=None):
        user = {
            'username': username,
            'email': email,
            'friends': {},
            'pp': self.__upload_user_pp(username, pp_path) if pp_path else ''
        }

        user_doc = self.__get_user_doc(username)
        user_doc.set(user)
        return response(201, user)

    def get_user(self, username):
        user_doc = self.__get_user_doc(username)
        user = user_doc.get().to_dict()
        if user: return response(200, user)
        return response(404, "user not found")

    def get_user_pp(self, username):
        user_doc = self.__get_user_doc(username)
        pp_link = user_doc.get(['pp']).to_dict()
        if pp_link: return response(200, pp_link)
        return response(404, "user not found")

    def update_user_pp(self, username, pp_path):
        pp_link = self.__upload_user_pp(username, pp_path)
        user_doc = self.__get_user_doc(username)

        pp = {
            'pp': pp_link
        }

        user_doc.update(pp)
        return response(201, pp)

    # Friends
    def get_all_friends(self, username):
        user_doc = self.__get_user_doc(username)
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
                400,
                "sender is already friends with dest or there is already a pending friend request between them"
            )
        
        friends[sender] = False
        user_doc.set({'friends': friends}, merge=True)
        return response(201, dest)

    def accept_friend_request(self, sender, dest):
        sender_doc = self.__get_user_doc(sender)
        if sender_doc.get().to_dict() is None: return response(404, "sender not found")
        
        dest_doc = self.__get_user_doc(dest)
        if dest_doc.get().to_dict() is None: return response(404, "dest not found")
    
        dest_friends = dest_doc.get().to_dict()['friends']
        if sender not in dest_friends or dest_friends[sender] == True:
            return response(400, "there is no pending friend request between sender and dest")
        
        sender_friends = sender_doc.get().to_dict()['friends']
        dest_friends[sender] = True
        dest_doc.set({'friends': dest_friends}, merge=True)
        sender_friends[dest] = True
        sender_doc.set({'friends': sender_friends}, merge=True)
        return response(201, sender)

    def delete_friend_or_friend_request(self, username, friend):
        user_doc = self.__get_user_doc(username)
        if user_doc.get().to_dict() is None: return response(404, "user not found")

        friend_doc = self.__get_user_doc(friend)
        user_friends = user_doc.get().to_dict()['friends']
        if friend not in user_friends:
            return response(
                400,
                "friend isn't a friend of user or there is no pending friend request between them"
            )
        
        friend_friends = friend_doc.get().to_dict()['friends']
        user_friends.pop(friend)
        temp = user_doc.get().to_dict()
        temp['friends'] = user_friends
        user_doc.set(temp)
        
        if username in friend_friends:
            friend_friends.pop(username)
            temp = friend_doc.get().to_dict()
            temp['friends'] = friend_friends
            friend_doc.set(temp)
        return response(200, friend)
