import logging
from flask_restful import Resource
from flask import request, abort, jsonify, make_response, g
from database import db
from models.profile_model import Profile
from models.account_model import Account
from models.access_model import Access
from schemas.profile_schema import profile_schema, profiles_schema
from schemas.access_schema import accesses_schema, access_schema
from services.variables import PROFILE_VALIDATED_GET_ARGS, ACCESS_VALIDATED_GET_ARGS, ACCESS_VALIDATED_ARGS, PROFILE_VALIDATED_ARGS
from services.methods import string_to_iso_format
from services.auth import is_admin

PROFILE_ENDPOINT = '/cam-api/v1/profile'


class ProfileResource(Resource):

    def __init__(self):
        self._admin_val = is_admin(g, ['admin', 'super-admin'])
        self._super_admin_val = is_admin(g, ['super-admin'])
        self._curr_account = g.cookie['user']['account']

    def get(self, profile_id=None):
        try:
            if not profile_id:
                args = {arg: request.args.get(arg) for arg in request.args if arg in PROFILE_VALIDATED_GET_ARGS}
                profiles = self._get_all(args)
                dumped = profiles_schema.dump(profiles)
            else:
                profile = self._get_by_id(profile_id)
                dumped = profile_schema.dump(profile)

            if not dumped:
                abort(400)

        except Exception as e:
            logging.warning(e)
            abort(400, "pas de profil correspondant")
        else:
            return make_response(jsonify({
                "status": "success",
                "message": "profil(s) récupéré(s)",
                "profile": dumped,
                "result": len(dumped)
            }), 200)

    def _get_all(self, data=None):
        profiles = Profile.query.filter_by(**data).all()
        return profiles

    def _get_by_id(self, profile_id):
        profile = Profile.query.filter_by(id=profile_id).first()
        return profile

    def post(self):
        json_data = request.get_json()
        if not json_data:
            abort(401, "data should be in json")
        try:
            # change date format of 'dob' to fit with db
            if 'dob' in json_data.keys():
                json_data['dob'] = string_to_iso_format(json_data['dob'])
            # validate fields from request
            val_data = {k: v for (k, v) in json_data.items() if k in PROFILE_VALIDATED_ARGS}
            # create new profile
            new_profile = profile_schema.load(val_data, session=db.session)
            # add profile to db
            db.session.add(new_profile)
            db.session.commit()

            # add link between profile and account to "access" table, take account_id from cookie
            val_access = {k: v for (k, v) in json_data.items() if k in ACCESS_VALIDATED_ARGS}
            val_access['account_id'] = g.cookie['user']['account']
            val_access['profile_id'] = new_profile.id
            new_access = access_schema.load(val_access, session=db.session)
            db.session.add(new_access)
            db.session.commit()
            # retrieve new profile infos to send to front
            p = profile_schema.dump(new_profile)

        except Exception as e:
            db.session.rollback()
            logging.warning(e)
            abort(403, f"Erreur: {e}")
        else:
            return make_response(jsonify({
                "status": "success",
                "message": "profil créé avec succès",
                "profile": p
            }), 201)

    def put(self, profile_id):
        json_data = request.get_json()
        if not json_data:
            abort(401, "data should be in json")
        try:
            # validate data
            profile_val_data = {k: v for (k, v) in json_data.items() if k in PROFILE_VALIDATED_ARGS}
            access_val_data = {k: v for (k, v) in json_data.items() if k in ACCESS_VALIDATED_ARGS}
            # retrieve profile
            profile = self._get_by_id(profile_id)
            if profile is None:
                abort(401, "Pas de profil correspondant")
            """
            UPDATE PROFILE
            """
            for k, v in profile_val_data.items():
                setattr(profile, k, v)
            db.session.commit()

            """
            UPDATE ACCESS
            """
            access = Access.query.get(profile_id=profile.id, account_id=self._curr_account).first()
            if access is None:
                abort(401, "Pas d'accès correspondant")
            else:
                # You must be at least admin to update an access
                if self._admin_val is True:
                    for k, v in access_val_data.items():
                        setattr(access, k, v)
                    db.session.commit()

            # dump profile to send to front
            pr = profile_schema.dump(profile)

        except Exception as e:
            db.session.rollback()
            logging.warning(e)
            abort(403, f"Probleme pour actualiser le profil: {e}")
        else:
            return make_response(jsonify({
                "status": "success",
                "message": "profil modifié avec succès",
                "profile": pr
            }), 200)

    def delete(self, profile_id):
        try:
            # Validate current user to be super admin to allow access
            if self._super_admin_val is False:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Accès non authorisé",
                }), 403)
            # retrieve profile to delete
            prof_to_del = self._get_by_id(profile_id)
            if prof_to_del is None:
                abort(401, "Pas de profil correspondant à l'id")
            else:
                # delete profile
                db.session.delete(prof_to_del)
                db.session.commit()
                
        except Exception as e:
            db.session.rollback()
            logging.warning(e)
            abort(403, f"Probleme pour supprimer le profil: {e}")
        else:
            return make_response(jsonify({
                "status": "success",
                "message": "profil supprimé avec succès",
            }), 200)

