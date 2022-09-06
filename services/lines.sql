DROP TABLES user, camera, locker, home, profile

from app import create_app
from database import db
from models.account_model import Account
from models.locker_model import Locker
from models.camera_model import Camera
from models.profile_model import Profile
from models.user_model import User
db.create_all(app=create_app())