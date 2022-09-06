from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.locker_model import Locker


class LockerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Locker
        include_fk = True,

