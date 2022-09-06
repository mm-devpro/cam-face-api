from models.profile_model import Profile
from database import ma


class ProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Profile
        include_fk = True,
        exclude = ("digit_pwd",)
