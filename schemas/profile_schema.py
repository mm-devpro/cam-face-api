from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.profile_model import Profile
from marshmallow import fields


class ProfileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Profile
        include_fk = True
        load_instance = True


profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)
