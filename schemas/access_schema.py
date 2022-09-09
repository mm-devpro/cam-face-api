from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from schemas.user_schema import UserSchema
from models.access_model import Access


class AccessSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Access
        load_instance = True
        include_fk = True
        include_relationships = True
        exclude = ("_password",)

    password = fields.Str()
    users = fields.List(fields.Nested(UserSchema))


access_schema = AccessSchema()
accesses_schema = AccessSchema(many=True)
