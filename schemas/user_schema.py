from models.user_model import User
from database import ma
from marshmallow import fields


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True,
        load_instance = True
        exclude = ("_password",)

    password = fields.Str(required=True)
