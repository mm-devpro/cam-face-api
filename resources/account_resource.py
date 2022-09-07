import logging
from flask_restful import Resource
from flask import request, abort, jsonify, g, make_response
from database import db
from models.account_model import Account
from schemas.account_schema import accounts_schema, account_schema

ACCOUNT_ENDPOINT = '/cam-api/v1/account'


class AccountResource(Resource):

    def get(self, account_id=None):
        try:
            if not account_id:
                args = {arg: request.args.get(arg) for arg in request.args if arg in ["name"]}
                accounts = self._get_all(args)
                dumped = accounts_schema.dump(accounts)
            else:
                account = self._get_by_id(account_id)
                dumped = account_schema.dump(account)

            if not dumped:
                abort(400)

        except Exception as e:
            logging.warning(e)
            abort(400, "pas de compte correspondant")
        else:
            return make_response(jsonify({
                "status": "success",
                "message": "compte(s) récupéré(s)",
                "account": dumped,
                "result": len(dumped)
            }), 200)

    def _get_all(self, data=None):
        if data:
            accounts = Account.query.filter_by(**data).all()
        else:
            accounts = Account.query.all()
        return accounts

    def _get_by_id(self, account_id):
        account = Account.query.filter_by(id=account_id).first()
        return account

    def post(self):
        json_data = request.get_json()
        if not json_data:
            abort(401, "data should be in json")
        try:
            ### validate data
            val_account = account_schema.dump(json_data)
            ### create new account
            new_account = account_schema.load(val_account, session=db.session)
            ### add to database
            db.session.add(new_account)
            db.session.commit()
            ### retrieve new user to send to front
            v = account_schema.dump(new_account)

        except Exception as e:
            db.session.rollback()
            logging.warning(e)
            abort(403, "Ce compte est deja existant")
        else:
            return make_response(jsonify({
                "status": "success",
                "message": "compte créé avec succès",
                "account": v
            }), 201)

    def put(self):
        pass

    def __del__(self):
        pass

