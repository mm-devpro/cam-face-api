from sqlalchemy.sql import func
from database import db
from services.variables import PROFILE_GROUP

access = db.Table('access', db.metadata,
                  db.Column('profile_id', db.Integer, db.ForeignKey('profile.id'), primary_key=True),
                  db.Column('account_id', db.Integer, db.ForeignKey('account.id'), primary_key=True),
                  db.Column('created_at', db.DateTime(timezone=True), server_default=func.now()),
                  db.Column('updated_at', db.DateTime(timezone=True), onupdate=func.now()),
                  db.Column('group', db.Enum(*PROFILE_GROUP), server_default="invite"),
                  db.Column('digit_pwd', db.Integer, default=0000, server_default="0000")
                  )
