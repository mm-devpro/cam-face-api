from sqlalchemy.sql import func
from database import db


class Profile(db.Model):
    __tablename__ = "profile"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    surname = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.Date(), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    access = db.relationship("Access", backref=db.backref('profile'), cascade='all, delete-orphan', lazy=True)

    def __repr__(self):
        return f'<Profile "{self.surname + self.name}...">'
