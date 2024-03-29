from flask import Flask, session
from flask_session import Session  # type: ignore

from flask_sqlalchemy import SQLAlchemy

from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from todo_api.config import App_Config


db = SQLAlchemy()

bcrypt = Bcrypt()

sess = Session()

mail = Mail()

ma = Marshmallow()


def create_app():
    """
    Create a new instance of the app with the given configuration.

    :param config_class: configuration class
    :return: app
    """
    # Initialize Flask-

    app = Flask(__name__)
    app.config.from_object(App_Config)
#     if app.config["SQLALCHEMY_DATABASE_URI"]:
#         print(f"using db")

    # Initialize SQLAlchemy
    db.init_app(app)

    # initialise seesion
    sess.init_app(app)

    # Initialize Bcrypt
    bcrypt.init_app(app)

    # Initialize Bcrypt
    mail.init_app(app)

    # Initialize Marshmallow
    ma.init_app(app)

    # Importing the models here so it can create the empty tables.
    # the routes

    from todo_api.users.views import users
    from todo_api.todo.views import todos

    app.register_blueprint(users)
    app.register_blueprint(todos)

    # create db tables from models if not exists
    with app.app_context():
        db.create_all()

    return app