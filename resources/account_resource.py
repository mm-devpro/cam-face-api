import logging
from flask_restful import Resource
from flask import request, abort, jsonify, g, make_response
from database import db
from models.account_model import Account
from schemas.account_schema import accounts_schema, account_schema

ACCOUNT_ENDPOINT = '/account'


class AccountResource(Resource):

    def get(self, locker_id=None):
        try:
            accounts = Account.query.all()
            dump_accounts = accounts_schema.dump(accounts)
        except Exception as e:
            pass
        else:
            return make_response(jsonify(dump_accounts))

    def post(self):
        try:
            req = request.get_json()
            new_account = account_schema.load(req, session=db.session)
            print(new_account)
            db.session.add(new_account)
            dumped_account = account_schema.dump(req)

        except Exception as e:
            db.session.rollback()
            logging.warning(e)
            abort(403, "Ce compte est deja existant")
        else:
            return make_response(dumped_account)

    def put(self):
        pass

    def __del__(self):
        pass

