from os import getenv, path
import sys
from database import db
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from dotenv import load_dotenv

from resources.account_resource import AccountResource, ACCOUNT_ENDPOINT


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
    CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

    # initiate app database
    with app.app_context():
        db.init_app(app)

    api = Api(app)

    # routes
    api.add_resource(AccountResource, ACCOUNT_ENDPOINT,  f"{ACCOUNT_ENDPOINT}/<account_id>")

    # blueprint for auth routes in our app
    # from routes.auth import auth as auth_blueprint
    # app.register_blueprint(auth_blueprint)
    # blueprint for non-auth parts of app
    # from routes.account import account as account_blueprint
    # app.register_blueprint(account_blueprint)


    # decoding cookie before each request
    # app.before_request_funcs.setdefault(None, [decode_cookie])
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
