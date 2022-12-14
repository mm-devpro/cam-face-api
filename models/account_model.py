from sqlalchemy.sql import func
from database import db


class Account(db.Model):
    """
    Account Flask-SQLAlchemy Model

    Represents object contained in account table
    """
    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    name = db.Column(db.String(255), nullable=False, unique=True)

    cameras = db.relationship("Camera", backref="account", cascade='all, delete-orphan', passive_deletes=True, lazy=True, uselist=True)
    lockers = db.relationship("Locker", backref="account", cascade='all, delete-orphan', passive_deletes=True, lazy=True, uselist=True)
    users = db.relationship("User", backref="account", cascade='all, delete-orphan', passive_deletes=True, lazy=True, uselist=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Account "{self.name}...">'
