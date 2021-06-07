from flask import Flask
from flask_cors import CORS
from flaskr.db import FireDB

# App creation
app = Flask(__name__)
CORS(app)

# DB init
db = FireDB()

# Import blueprints
from flaskr import home, users, friends, groups

app.register_blueprint(home.bp)
app.register_blueprint(users.bp)
app.register_blueprint(friends.bp)
app.register_blueprint(groups.bp)
