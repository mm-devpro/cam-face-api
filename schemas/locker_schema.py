from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from schemas.camera_schema import CameraSchema
from models.locker_model import Locker


class LockerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Locker
        load_instance = True
        include_fk = True
        include_relationships = True

    camera = fields.Nested(CameraSchema)


locker_schema = LockerSchema()
lockers_schema = LockerSchema(many=True)
