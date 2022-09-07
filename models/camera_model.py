from database import db


class Camera(db.Model):
    """
    Camera Flask-SQLAlchemy Model

    Represents object contained in camera table
    """
    __tablename__ = "camera"

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=False, server_default="0")

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    locker_id = db.Column(db.Integer, db.ForeignKey('locker.id'), nullable=False)

    def __repr__(self):
        return f'<Camera "{self.source}...">'

