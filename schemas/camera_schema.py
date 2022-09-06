from models.camera_model import Camera
from database import ma


class CameraSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Camera
        include_fk = True,

