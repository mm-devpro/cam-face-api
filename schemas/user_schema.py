from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from models.user_model import User


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True
        include_relationships = True
        exclude = ("_password",)

    password = fields.Str(required=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)

