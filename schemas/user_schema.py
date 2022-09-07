from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from models.user_model import User


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        load_instance = True
        exclude = ("_password",)

    password = fields.Str(required=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)

