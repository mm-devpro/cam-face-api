import pickle
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from schemas.access_schema import AccessSchema
from models.profile_model import Profile


class ProfileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Profile
        load_instance = True
        include_fk = True
        include_relationships = True
    access = fields.List(fields.Nested(AccessSchema(only=('group', 'account_id',))))


profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)
