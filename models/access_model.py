from sqlalchemy.sql import func
from database import db
from services.variables import PROFILE_GROUP


class Access(db.Model):
    __tablename__ = "access"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    group = db.Column(db.Enum(*PROFILE_GROUP), server_default="invite")
    digit_pwd = db.Column(db.String(4), server_default="1234")

    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def __repr__(self):
        return f'<Profile "{self.surname + self.name}...">'
