from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func

from database import db
from services.variables import USER_ROLES, ADMIN_ROLES


class User(db.Model):
    """
    User Flask-SQLAlchemy Model

    Represents object contained in user table
    """
    __tablename__ = "user"
    # takes into account google/email authentication
    # __table_args__ = (db.UniqueConstraint("google_id"), db.UniqueConstraint("email"))
    # google_id = db.Column(db.String(100), nullable=True)
    # activated = db.Column(db.Boolean, default=False, server_default="0", nullable=False)

    id = db.Column(db.Integer, primary_key=True)
    # if user sets up his account within the app
    _password = db.Column(db.String(500), nullable=False)

    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True)
    role = db.Column(db.Enum(*USER_ROLES, *ADMIN_ROLES), server_default="user")
    img = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    last_login = db.Column(db.DateTime(timezone=True), nullable=True)

    account_id = db.Column(db.Integer, db.ForeignKey("account.id"))

    def __repr__(self):
        return f'<User "{self.username}...">'

    @property
    def password(self):
        raise AttributeError("Can't read password")

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self._password, password)
