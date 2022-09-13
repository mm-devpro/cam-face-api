from sqlalchemy.sql import func
from database import db
from services.variables import PROFILE_GROUP, LOCKER_ACCESS


class Access(db.Model):
    __tablename__ = "access"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    group = db.Column(db.Enum(*PROFILE_GROUP.keys()), server_default="inv")
    _password = db.Column(db.String(6), server_default="123456")
    access_lvl = db.Column(db.Enum(*LOCKER_ACCESS.keys()), nullable=False, server_default="0")

    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id", ondelete="CASCADE"), nullable=False,)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f'<Profile "{self.surname + self.name}...">'

    @property
    def password(self):
        raise AttributeError("Can't read password")

    @password.setter
    def password(self, password):
        self._password = password

    def verify_password(self, password):
        return self._password == password

