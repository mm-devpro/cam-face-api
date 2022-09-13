from database import db


class Camera(db.Model):
    """
    Camera Flask-SQLAlchemy Model

    Represents object contained in camera table
    """
    __tablename__ = "camera"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, server_default="camera")
    source = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=False, server_default="0")

    account_id = db.Column(db.Integer, db.ForeignKey("account.id", ondelete="CASCADE"))
    locker_id = db.Column(db.Integer, db.ForeignKey("locker.id"), nullable=True)

    def __repr__(self):
        return f'<Camera "{self.source}...">'

