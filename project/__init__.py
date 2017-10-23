import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# instantiate the db

db = SQLAlchemy()


def create_app():
    # instantiate the application
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extension
    db.init_app(app)

    # register blueprints
    from project.api.views import user_blueprint

    app.register_blueprint(user_blueprint)

    return app
