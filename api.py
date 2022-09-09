from os import getenv, path
import sys
from flask import Flask, Response, request
from flask_cors import CORS
from flask_restful import Api
from dotenv import load_dotenv
from database import db
from services.auth import decode_cookie
from resources.access_resource import AccessResource, ACCESS_ENDPOINT
from resources.camera_resource import CameraResource, StreamResource, CAMERA_ENDPOINT, STREAM_ENDPOINT
from resources.locker_resource import LockerResource, LOCKER_ENDPOINT
from resources.account_resource import AccountResource, ACCOUNT_ENDPOINT
from resources.auth_resource import LoginResource, LogoutResource, SignupResource, LOGOUT_ENDPOINT, LOGIN_ENDPOINT, \
    SIGNUP_ENDPOINT
from resources.profile_resource import ProfileResource, PROFILE_ENDPOINT
from resources.user_resource import UserResource, USER_ENDPOINT
from resources.stream_handler import StreamHandler

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

load_dotenv()
DB_USER = getenv('DB_USER')
DB_PWD = getenv('DB_PWD')
SECRET_KEY = getenv('SECRET_KEY')
MYSQL_URL = getenv('MYSQL_URL')
MYSQL_DB = getenv('MYSQL_DB')
MYSQL_PORT = getenv('MYSQL_PORT')
JWT_SECRET_KEY = getenv('JWT_SECRET_KEY')


def create_app():
    # initiate app variable
    app = Flask(__name__)
    # app configuration
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PWD}@{MYSQL_URL}:{MYSQL_PORT}/{MYSQL_DB}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # initiate api from flask-restful, and add cors configuration
    # api = Api(app)
    CORS(app, resources={r"/cam-api/v1/*": {"origins": "*"}})

    # initiate app database
    with app.app_context():
        db.init_app(app)

    api = Api(app)

    # routes
    api.add_resource(AccessResource, ACCESS_ENDPOINT, f"{ACCESS_ENDPOINT}/<access_id>")
    api.add_resource(AccountResource, ACCOUNT_ENDPOINT, f"{ACCOUNT_ENDPOINT}/<account_id>")
    api.add_resource(CameraResource, CAMERA_ENDPOINT, f"{CAMERA_ENDPOINT}/<camera_id>")
    api.add_resource(LockerResource, LOCKER_ENDPOINT, f"{LOCKER_ENDPOINT}/<locker_id>")
    api.add_resource(LoginResource, LOGIN_ENDPOINT)
    api.add_resource(LogoutResource, LOGOUT_ENDPOINT)
    api.add_resource(ProfileResource, PROFILE_ENDPOINT, f"{PROFILE_ENDPOINT}/<profile_id>")
    api.add_resource(SignupResource, SIGNUP_ENDPOINT)
    api.add_resource(UserResource, USER_ENDPOINT, f"{USER_ENDPOINT}/<user_id>")
    api.add_resource(StreamResource, STREAM_ENDPOINT)

    # decoding cookie before each request
    app.before_request_funcs.setdefault(None, [decode_cookie])

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
