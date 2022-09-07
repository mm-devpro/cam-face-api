from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.camera_model import Camera


class CameraSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Camera
        include_fk = True
        include_relationships = True


camera_schema = CameraSchema()
cameras_schema = CameraSchema(many=True)