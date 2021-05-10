from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "youtube.db"

UPLOAD_FOLDER_VIDEO = os.path.join(
    os.getcwd(), 'C:/Users/Ram Sharma/Desktop/python/youtube/static/video_upload')
UPLOAD_FOLDER_VIDEO_THUMBNAIL = os.path.join(
    os.getcwd(), 'C:/Users/Ram Sharma/Desktop/python/youtube/static/video_thumbnail')
UPLOAD_FOLDER_PROFILE_IMAGE = os.path.join(
    os.getcwd(), 'C:/Users/Ram Sharma/Desktop/python/youtube/static/profile_image')
UPLOAD_FOLDER_COVER_IMAGE = os.path.join(
    os.getcwd(), 'C:/Users/Ram Sharma/Desktop/python/youtube/static/cover_image')
ALLOWED_EXTENSIONS_IMAGE = {'png', 'jpg', 'jpeg'}
ALLOWED_EXTENSIONS_VIDEO = {'mp4'}


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'youtubesecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/youtube'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .upload_video import upload_video
    from .setting import setting

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(upload_video, url_prefix='/')
    app.register_blueprint(setting, url_prefix='/')

    from .models import Channel

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Channel.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('youtube/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
