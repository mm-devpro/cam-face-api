import logging
from flask_restful import Resource
from flask import request, abort, jsonify, g, make_response
from database import db
from models.profile_model import Profile
from schemas.profile_schema import profile_schema, profiles_schema
from services.variables import PROFILE_VALIDATED_QUERY_ARGS

PROFILE_ENDPOINT = '/cam-api/v1/profile'


class ProfileResource(Resource):

    def get(self, profile_id=None):
        try:
            if not profile_id:
                args = {arg: request.args.get(arg) for arg in request.args if arg in PROFILE_VALIDATED_QUERY_ARGS}
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
                "profile": dumped
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
            new_profile = profile_schema.load(json_data, session=db.session)

            db.session.add(new_profile)
            db.session.commit()
            dumped_profile = profile_schema.dump(new_profile)

        except Exception as e:
            db.session.rollback()
            logging.warning(e)
            abort(403, "Ce profil est deja existant")
        else:
            return make_response(jsonify({
                "status": "success",
                "message": "profil créé avec succès",
                "profile": dumped_profile
            }), 201)

    def put(self):
        pass

    def __del__(self):
        pass

