from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.account_model import Account


class AccountSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Account
        include_fk = True
        load_instance = True


account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)
