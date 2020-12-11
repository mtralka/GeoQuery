import os

from celery import Celery
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

celery = Celery(
    __name__, broker=os.environ.get("CELERY_BROKER"), backend=os.environ.get("CELERY_BACKEND")
)


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")

    # CELERY INIT
    celery.conf.update(app.config)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .model import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # blue auth
    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    # blue main
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .api_endpoint import api_endpoint as api_endpoint_blueprint

    app.register_blueprint(api_endpoint_blueprint)

    return app
