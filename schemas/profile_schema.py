from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.profile_model import Profile


class ProfileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Profile
        include_fk = True,


profile_schema = ProfileSchema()
profiles_schema = ProfileSchema(many=True)