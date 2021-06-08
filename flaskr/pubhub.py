from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from dotenv import load_dotenv
import os
from random import choice
from string import digits, ascii_letters

load_dotenv()

def get_auth_key():
    return ''.join(choice(ascii_letters + digits) for i in range(64))

pnconfig = PNConfiguration()
pnconfig.publish_key = os.environ['PN_PUBLISH_KEY']
pnconfig.subscribe_key = os.environ['PN_SUBSCRIBE_KEY']
pnconfig.secret_key = os.environ['PN_SECRET_KEY']
pnconfig.uuid = os.environ['PN_SERVER_UUID']

pubnub = PubNub(pnconfig)

pubnub.grant()\
    .auth_keys("4N4h7YYkpIkZunkAO1F5BthvlAwWN8vKYDoboZdBw2VHzXZadm8xtC6RWj8SEVLy")\
    .channels(["uwu"])\
    .read(True)\
    .write(True)

