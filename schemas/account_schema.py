from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from schemas.locker_schema import LockerSchema
from schemas.user_schema import UserSchema
from schemas.camera_schema import CameraSchema
from models.account_model import Account


class AccountSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Account
        load_instance = True
        include_fk = True
        include_relationships = True

    users = fields.List(fields.Nested(UserSchema))
    cameras = fields.List(fields.Nested(CameraSchema))
    lockers = fields.List(fields.Nested(LockerSchema))


account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)
