from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from models.locker_model import Locker
from schemas.camera_schema import CameraSchema


class LockerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Locker
        include_fk = True
        include_relationships = True

    camera = fields.Nested(CameraSchema)


locker_schema = LockerSchema()
lockers_schema = LockerSchema(many=True)
