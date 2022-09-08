import logging
from flask_restful import Resource
from flask import request, abort, jsonify, g, make_response
from database import db
from models.account_model import Account
from schemas.account_schema import accounts_schema, account_schema
from services.variables import ACCOUNT_VALIDATED_ARGS, ACCOUNT_VALIDATED_GET_ARGS

ACCOUNT_ENDPOINT = '/cam-api/v1/account'


class AccountResource(Resource):

    def get(self, curr=False):
        try:
            if curr:
                account = self._get_curr()
                dumped = account_schema.dump(account)
            else:
                args = {arg: request.args.get(arg) for arg in request.args if arg in ACCOUNT_VALIDATED_GET_ARGS}
                accounts = self._get_all(args)
                dumped = accounts_schema.dump(accounts)

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
        accounts = Account.query.filter_by(**data).all()
        return accounts

    def _get_curr(self):
        account = Account.query.filter_by(id=g.cookie['user']['account']).first()
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
            ### retrieve new account to send to front
            a = account_schema.dump(new_account)

        except Exception as e:
            db.session.rollback()
            logging.warning(e)
            abort(403, "Ce compte est deja existant")
        else:
            return make_response(jsonify({
                "status": "success",
                "message": "compte créé avec succès",
                "account": a
            }), 201)

    def put(self, account_id=None):
        json_data = request.get_json()
        if not json_data:
            abort(401, "data should be in json")
        try:
            ### validate data
            val_data = {k: v for (k, v) in json_data.items() if k in ACCOUNT_VALIDATED_ARGS}
            ### retrieve chosen or current account
            if account_id is not None:
                account = Account.query.filter_by(id=account_id).first()
            else:
                account = self._get_curr()
            ### update account with new values
            for k, v in val_data.items():
                setattr(account, k, v)
            db.session.commit()
            ### dump account to send to front
            a = account_schema.dump(account)
        except Exception as e:
            db.session.rollback()
            logging.warning(e)
            abort(403, f"Probleme pour actualiser le compte: {e}")
        else:
            return make_response(jsonify({
                "status": "success",
                "message": "compte modifié avec succès",
                "account": a
            }), 200)

    def delete(self, account_id):
        try:
            acc_to_del = Account.query.filter_by(id=account_id).first()
            if acc_to_del is None:
                abort(403, "Pas de compte correspondant à l'id")
            else:
                db.session.delete(acc_to_del)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.warning(e)
            abort(403, f"Probleme pour supprimer le compte: {e}")
        else:
            return make_response(jsonify({
                "status": "success",
                "message": "compte supprimé avec succès",
            }), 200)
