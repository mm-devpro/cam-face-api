from models.locker_model import Locker
from database import ma


class LockerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Locker
        include_fk = True,

