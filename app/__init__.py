from celery import Celery
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

celery = Celery(
    __name__, broker="redis://localhost:6379/0", backend="redis://localhost:6379/0"
)


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "SECRETKEY"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    
    # abs path for results serving
    app.config["RESULTS"] = "C:\\Users\\mtral\\Documents\\GitHub\\matthewtralka_MnM4SDS_project\\response"

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

    return app
