import logging
from flask_restful import Resource
from flask import request, abort, jsonify, g, make_response
from database import db
from models.locker_model import Locker
from schemas.locker_schema import lockers_schema, locker_schema
from services.variables import LOCKER_VALIDATED_GET_ARGS, LOCKER_VALIDATED_ARGS
from services.auth import is_admin

LOCKER_ENDPOINT = '/cam-api/v1/locker'


class LockerResource(Resource):

    def __init__(self):
        self._admin_val = is_admin(g, ['admin', 'super-admin'])
        self._super_admin_val = is_admin(g, ['super-admin'])
        self._curr_account = g.cookie['user']['account']

    def get(self, locker_id=None):
        try:
            if not locker_id:
                args = {arg: request.args.get(arg) for arg in request.args if arg in LOCKER_VALIDATED_GET_ARGS}
                lockers = self._get_all(args)
                dumped = lockers_schema.dump(lockers)
            else:
                locker = self._get_by_id(locker_id)
                dumped = locker_schema.dump(locker)

            if not dumped:
                abort(400)

        except Exception as e:
            logging.warning(e)
            abort(400, "pas de locker correspondant")
        else:
            return make_response(jsonify({
                "status": "success",
                "message": "locker(s) récupéré(s)",
                "locker": dumped,
                "result": len(dumped)
            }), 200)

    def _get_all(self, data=None):
        # Only get lockers for the current account
        lockers = Locker.query.filter_by(account_id=self._curr_account, **data).all()
        return lockers

    def _get_by_id(self, locker_id):
        locker = Locker.query.filter_by(account_id=self._curr_account, id=locker_id).first()
        return locker

    def post(self):
        json_data = request.get_json()
        if not json_data:
            abort(401, "data should be in json")
        try:
            # Must be at least admin to post a locker
            if self._admin_val is False:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Accès non authorisé",
                }), 403)
            # validate data
            val_data = {k: v for (k, v) in json_data.items() if k in LOCKER_VALIDATED_GET_ARGS}
            # create new locker
            new_locker = locker_schema.load(val_data, session=db.session)
            # add to database
            db.session.add(new_locker)
            # link new locker to current account
            new_locker.account_id = self._curr_account
            db.session.commit()
            # retrieve new locker to send to front
            lo = locker_schema.dump(new_locker)

        except Exception as e:
            db.session.rollback()
            logging.warning(e)
            abort(403, "Ce locker est deja existant")
        else:
            return make_response(jsonify({
                "status": "success",
                "message": "locker créé avec succès",
                "locker": lo
            }), 201)

    def put(self, locker_id):
        json_data = request.get_json()
        if not json_data:
            abort(401, "data should be in json")
        try:
            # Must be at least admin to update locker
            if self._admin_val is False:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Accès non authorisé",
                }), 403)
            # validate data
            val_data = {k: v for (k, v) in json_data.items() if k in LOCKER_VALIDATED_ARGS}
            # retrieve locker
            locker = self._get_by_id(locker_id)
            # check if locker exists
            if locker is None:
                abort(404, f"Pas de locker correspondant")
            # validate that locker is from the same account as current to allow update
            elif locker.account_id != self._curr_account:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Accès non authorisé",
                }), 403)
            else:
                # update data
                for k, v in val_data.items():
                    setattr(locker, k, v)
                db.session.commit()

            # dump new locker to send to front
            lo = locker_schema.dump(locker)
        except Exception as e:
            db.session.rollback()
            logging.warning(e)
            abort(403, f"Probleme pour actualiser le locker: {e}")
        else:
            return make_response(jsonify({
                "status": "success",
                "message": "locker modifié avec succès",
                "locker": lo
            }), 200)

    def delete(self, locker_id):
        try:
            # Validate current user to be at least admin to allow access
            if self._admin_val is False:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Accès non authorisé",
                }), 403)
            # retrieve locker
            loc_to_del = self._get_by_id(locker_id)
            # check if locker exists
            if loc_to_del is None:
                abort(404, f"Pas de locker correspondant")
            # validate that locker is from the same account as current to allow deletion
            elif loc_to_del.account_id != self._curr_account:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Accès non authorisé",
                }), 403)
            else:
                db.session.delete(loc_to_del)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.warning(e)
            abort(403, f"Probleme pour actualiser le locker: {e}")
        else:
            return make_response(jsonify({
                "status": "success",
                "message": "locker supprimé avec succès",
            }), 200)
