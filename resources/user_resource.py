import logging
from flask_restful import Resource
from flask import request, abort, jsonify, g, make_response
from database import db
from models.user_model import User
from schemas.user_schema import users_schema, user_schema
from services.variables import USER_VALIDATED_GET_ARGS

USER_ENDPOINT = '/cam-api/v1/user'


class UserResource(Resource):

    def get(self, user_id=None):
        try:
            if not user_id:
                args = {arg: request.args.get(arg) for arg in request.args if arg in USER_VALIDATED_GET_ARGS}
                users = self._get_all(args)
                dumped = users_schema.dump(users)
            else:
                user = self._get_by_id(user_id)
                dumped = user_schema.dump(user)

            if not dumped:
                abort(400)

        except Exception as e:
            logging.warning(e)
            abort(400, "pas d'utilisateur correspondant")
        else:
            return make_response(jsonify({
                "status": "success",
                "message": "utilisateur(s) récupéré(s)",
                "user": dumped,
                "result": len(dumped)
            }), 200)

    def _get_all(self, data=None):
        # get Users from the current account
        users = User.query.filter_by(account_id=g.cookie['user']['account'], **data).all()
        return users

    def _get_by_id(self, user_id):
        # Get User for the current account
        user = User.query.filter_by(account_id=g.cookie['user']['account'], id=user_id).first()
        return user

    def post(self):
        json_data = request.get_json()
        if not json_data:
            abort(401, "data should be in json")
        try:
            ### field validation (removing potential bad fields from request)
            val_user = user_schema.dump(json_data)
            ### load new user
            new_user = user_schema.load(val_user, session=db.session)
            ### add new user to db
            db.session.add(new_user)
            ### link new user to current account
            new_user.account_id = g.cookie['user']['account']
            db.session.commit()
            ### get new user infos to send to front
            u = user_schema.dump(new_user)

        except Exception as e:
            db.session.rollback()
            logging.warning(e)
            abort(403, "Cet utilisateur est deja existant")
        else:
            return make_response(jsonify({
                "status": "success",
                "message": "utilisateur créé avec succès",
                "user": u
            }), 201)

    def put(self):
        pass

    def delete(self):
        pass

