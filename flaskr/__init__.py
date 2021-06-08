import os

from flask import Flask
from flask_cors import CORS
from flaskr.db import FireDB

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from dotenv import load_dotenv


# App creation
app = Flask(__name__)
CORS(app)

# DB init
db = FireDB()

# Pubnub init
load_dotenv()

pnconfig = PNConfiguration()
pnconfig.publish_key = os.environ['PN_PUBLISH_KEY']
pnconfig.subscribe_key = os.environ['PN_SUBSCRIBE_KEY']
pnconfig.secret_key = os.environ['PN_SECRET_KEY']
pnconfig.uuid = os.environ['PN_SERVER_UUID']

pubnub = PubNub(pnconfig)

# Import blueprints
from flaskr import home, users, friends, groups, auth

app.register_blueprint(home.bp)
app.register_blueprint(users.bp)
app.register_blueprint(friends.bp)
app.register_blueprint(groups.bp)
app.register_blueprint(auth.bp)
