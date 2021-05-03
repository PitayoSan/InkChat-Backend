import os
import firebase_admin

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
        user_doc = self.__get_user_doc(username)
        user_doc.set({
            'username': username,
            'email': email,
            'friends': {},
            'pp': self.__upload_user_pp(username, pp_path) if pp_path else ''
        })
        
        return username

    def get_user(self, username):
        user_doc = self.__get_user_doc(username)
        user = user_doc.get().to_dict()
        return user

    def get_user_pp(self, username):
        user_doc = self.__get_user_doc(username)
        pp_link = user_doc.get('pp')
        return pp_link

    def update_user_pp(self, username, pp_path):
        pp_link = self.__upload_user_pp(username, pp_path)
        user_doc = self.__get_user_doc(username)
        user_doc.update({
            'pp': pp_link
        })
        return pp_link

    # Friends
    def get_all_friends(self, username):
        user_doc = self.__get_user_doc(username)
        friends = user_doc.get().to_dict()['friends']
        return friends

    def send_friend_request(self, sender, dest):
        user_doc = self.__get_user_doc(dest)
        friends = user_doc.get().to_dict()['friends']
        if sender in friends:
            return 'ERROR: sender is already friends with dest or there is already a pending friend request between them.'
        friends[sender] = False
        user_doc.set({'friends': friends}, merge=True)
        return dest

    def accept_friend_request(self, sender, dest):
        dest_doc = self.__get_user_doc(dest)
        dest_friends = dest_doc.get().to_dict()['friends']
        if sender not in dest_friends:
            return 'ERROR: there is no pending friend request between sender and dest.'
        dest_friends[sender] = True
        dest_doc.set({'friends': dest_friends}, merge=True)

        sender_doc = self.__get_user_doc(sender)
        sender_friends = sender_doc.get().to_dict()['friends']
        sender_friends[dest] = True
        sender_doc.set({'friends': sender_friends}, merge=True)
        return sender

    def delete_friend_or_friend_request(self, username, friend):
        user_doc = self.__get_user_doc(username)
        user_friends = user_doc.get().to_dict()['friends']
        if friend not in user_friends:
            return 'ERROR: friend isn\'t a friend of user or there is no pending friend request between them.'
        user_friends.pop(friend)
        temp = user_doc.get().to_dict()
        temp['friends'] = user_friends
        user_doc.set(temp)
        
        friend_doc = self.__get_user_doc(friend)
        friend_friends = friend_doc.get().to_dict()['friends']
        if user in friend_friends:
            friend_friends.pop(user)
            temp = friend_doc.get().to_dict()
            temp['friends'] = friend_friends
            friend_doc.set(temp)
        return friend
    
