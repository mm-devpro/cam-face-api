import logging
from flask_restful import Resource
from flask import request, abort, jsonify, make_response
from database import db
from models.profile_model import Profile
from models.account_model import Account
from models.access_model import Access
from schemas.profile_schema import profile_schema, profiles_schema
from schemas.access_schema import accesses_schema, access_schema
from services.variables import PROFILE_VALIDATED_GET_ARGS, ACCESS_VALIDATED_GET_ARGS
from services.methods import string_to_iso_format

PROFILE_ENDPOINT = '/cam-api/v1/profile'


class ProfileResource(Resource):

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
        if data:
            profiles = Profile.query.filter_by(**data).all()
        else:
            profiles = Profile.query.all()
        return profiles

    def _get_by_id(self, profile_id):
        profile = Profile.query.filter_by(id=profile_id).first()
        return profile

    def post(self):
        json_data = request.get_json()
        if not json_data:
            abort(401, "data should be in json")
        try:
            ### change date format of 'dob' to fit with db
            if 'dob' in json_data.keys():
                json_data['dob'] = string_to_iso_format(json_data['dob'])
            ### validate fields from request
            val_data = {k: v for (k, v) in json_data.items() if k in PROFILE_VALIDATED_GET_ARGS}
            ### create new profile
            new_profile = profile_schema.load(val_data, session=db.session)
            ### add profile to db
            db.session.add(new_profile)
            ### add link between profile and account to "access" table, take account_id from cookie
            if 'account_id' in json_data.keys():
                account_id = json_data['account_id']
                account = Account.query.filter_by(id=account_id).first()
                if account is not None:
                    val_access = {k: v for (k, v) in json_data.items() if k in ACCESS_VALIDATED_GET_ARGS}
                    val_access['account_id'] = account_id
                    val_access['profile_id'] = new_profile.id
                    new_access = access_schema.load(val_access, session=db.session)
                    db.session.add(new_access)
            db.session.commit()
            ### retrieve new profile infos to send to front
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

    def put(self):
        pass

    def __del__(self):
        pass

