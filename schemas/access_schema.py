from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.access_model import Access
from schemas.user_schema import UserSchema
from marshmallow import fields


class AccessSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Access
        load_instance = True
        include_fk = True
        include_relationships = True
    users = fields.List(fields.Nested(UserSchema))

access_schema = AccessSchema()
accesses_schema = AccessSchema(many=True)
