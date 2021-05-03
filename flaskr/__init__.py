from flask import Flask
from flask_cors import CORS


def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)

    # Import blueprints
    from . import home, users, friends, test

    app.register_blueprint(home.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(friends.bp)
    app.register_blueprint(test.bp)

    return app
