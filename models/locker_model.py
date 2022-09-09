from database import db
from services.variables import LOCKER_TYPE, LOCKER_ACCESS


class Locker(db.Model):
    """
    Locker Flask-SQLAlchemy Model

    Represents object contained in locker table
    """
    __tablename__ = "locker"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    access_lvl = db.Column(db.Enum(*LOCKER_ACCESS.keys()), nullable=False, server_default="0")
    type = db.Column(db.Enum(*LOCKER_TYPE), server_default="door")
    locked = db.Column(db.Boolean, default=True, server_default="1")
    digit_activation = db.Column(db.Boolean, default=True, server_default="1")

    account_id = db.Column(db.Integer, db.ForeignKey("account.id"))
    camera = db.relationship("Camera", backref=db.backref("locker"), lazy=True, uselist=False)

    def __repr__(self):
        return f'<Locker "{self.name}...">'

