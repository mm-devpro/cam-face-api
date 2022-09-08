import logging
from flask_restful import Resource
from flask import request, abort, jsonify, g, make_response
from database import db
from models.access_model import Access
from schemas.access_schema import accesses_schema, access_schema
from services.variables import ACCESS_VALIDATED_ARGS, ACCESS_VALIDATED_GET_ARGS
from services.auth import is_admin

ACCESS_ENDPOINT = '/cam-api/v1/access'


class AccessResource(Resource):

    def __init__(self):
        self._admin_val = is_admin(g, ['admin', 'super-admin'])
        self._super_admin_val = is_admin(g, ['super-admin'])
        self._curr_account = g.cookie['user']['account']

    def get(self, access_id):
        """
        GET Method to get access infos
        :param access_id:
        :return:
        """
        try:
            access = self._get_by_id(access_id)
            if access is None:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Accès non authorisé",
                }), 403)
            dumped = access_schema.dump(access)
            if not dumped:
                abort(400)

        except Exception as e:
            logging.warning(e)
            abort(400, "pas de access correspondante")
        else:
            return make_response(jsonify({
                "status": "success",
                "message": "access(s) récupéré(s)",
                "access": dumped,
                "result": len(dumped)
            }), 200)

    def _get_by_id(self, access_id):
        # Get access from profile
        profile_id = request.args.get('profile_id')
        if profile_id is None:
            abort(401, "Pas de profil identifié")
        access = Access.query.filter_by(id=access_id, profile_id=profile_id, account_id=self._curr_account).first()
        return access

    def post(self):
        json_data = request.get_json()
        if not json_data:
            abort(401, "data should be in json")
        try:
            # validate data
            val_data = {k: v for (k, v) in json_data.items() if k in ACCESS_VALIDATED_ARGS}
            # get corresponding profile
            profile_id = request.args.get('profile_id')
            if profile_id is None:
                abort(401, "Pas de profil identifié")
            # create new access
            new_access = access_schema.load(val_data, session=db.session)
            # link access to current account / profile
            new_access.profile_id = profile_id
            new_access.account_id = self._curr_account
            # add to database
            db.session.add(new_access)
            db.session.commit()

            # dump new access to send to front
            a = access_schema.dump(new_access)

        except Exception as e:
            db.session.rollback()
            logging.warning(e)
            abort(403, "Cet accès est deja existant")
        else:
            return make_response(jsonify({
                "status": "success",
                "message": "accès créée avec succès",
                "access": a
            }), 201)

    def put(self, access_id):
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
            val_data = {k: v for (k, v) in json_data.items() if k in access_VALIDATED_ARGS}
            # retrieve access
            access = self._get_by_id(access_id)
            # check if access exists
            if access is None:
                abort(404, f"Pas de access correspondant")
            # validate that access is from the same account as current to allow update
            elif access.account_id != self._curr_account:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Accès non authorisé",
                }), 403)
            else:
                # update data
                for k, v in val_data.items():
                    setattr(access, k, v)
                db.session.commit()

            # dump new access to send to front
            cam = access_schema.dump(access)
        except Exception as e:
            db.session.rollback()
            logging.warning(e)
            abort(403, f"Probleme pour actualiser la access: {e}")
        else:
            return make_response(jsonify({
                "status": "success",
                "message": "access modifié avec succès",
                "access": cam
            }), 200)

    def delete(self, access_id):
        try:
            # Validate current user to be at least admin to allow access
            if self._admin_val is False:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Accès non authorisé",
                }), 403)
            # retrieve access
            access_to_del = self._get_by_id(access_id)
            # check if access exists
            if access_to_del is None:
                abort(404, f"Pas de access correspondant")
            # validate that access is from the same account as current to allow deletion
            elif access_to_del.account_id != self._curr_account:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Accès non authorisé",
                }), 403)
            else:
                db.session.delete(access_to_del)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.warning(e)
            abort(403, f"Probleme pour actualiser l'access: {e}")
        else:
            return make_response(jsonify({
                "status": "success",
                "message": "access supprimé avec succès",
            }), 200)

