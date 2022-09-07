from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from models.account_model import Account
from schemas.user_schema import UserSchema
from schemas.locker_schema import LockerSchema
from schemas.camera_schema import CameraSchema


class AccountSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Account
        include_fk = True
        load_instance = True
        include_relationships = True

    users = fields.List(fields.Nested(UserSchema))
    lockers = fields.List(fields.Nested(LockerSchema))
    cameras = fields.List(fields.Nested(CameraSchema))


account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)
