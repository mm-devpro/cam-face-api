import logging
from flask_restful import Resource
from flask import request, abort, jsonify, g, make_response
from database import db
from models.user_model import User
from schemas.user_schema import users_schema, user_schema
from services.auth import set_token_in_cookie

LOGIN_ENDPOINT = '/cam-api/v1/login'
LOGOUT_ENDPOINT = '/cam-api/v1/logout'
SIGNUP_ENDPOINT = '/cam-api/v1/signup'


class LoginResource(Resource):

    def post(self):
        """
        LoginResource LOGIN method. Check user credentials and validate or not
        :return: user infos, token in cookie
        """
        # get json data
        json_data = request.get_json()
        if not json_data:
            abort(401, "data should be in json")
        try:
            ### validate data with UserSchema
            valid_data = user_schema.dump(json_data)

            ### 1) Check if user is in the db
            user = User.query.filter(User.email == valid_data['email']).first()
            if user is None:
                logging.warning("Pas d'utilisateur correspondant")
                return make_response(jsonify({
                    "status": "error",
                    "message": "Error with user credentials"
                }), 403)

            ### 2) Check if password is good
            if user.verify_password(valid_data['password']) is False:
                logging.warning("Error with user credentials")
                return make_response(jsonify({
                    "status": "error",
                    "message": "Error with user credentials"
                }), 403)

        except Exception as e:
            db.session.rollback()
            logging.warning(e)
            abort(403, "Identifiants non valides, réessayer ultérieurement")
        else:
            ### set token in cookie and send user infos to front
            return set_token_in_cookie(user)


class LogoutResource(Resource):

    def post(self):
        g.cookie = {}
        response = make_response("Logged out", 200)
        response.set_cookie("user", "")
        return response


class SignupResource(Resource):

    def post(self):
        # get json data
        json_data = request.get_json()
        if not json_data:
            abort(401, "data should be in json")
        try:
            ### 1) Validate fields from request
            val_user = user_schema.dump(json_data)
            ### 2) create new user
            new_user = user_schema.load(val_user, session=db.session)
            ### 3) Check if user is not in the db
            user = User.query.filter(User.email == new_user.email).first()
            if user is not None:
                logging.warning("This user already exists")
                return make_response(jsonify({
                    "status": "error",
                    "message": "Cet utilisateur existe deja, veuillez vous connecter à la place"
                }), 401)
            ### 4) Add user to db
            db.session.add(new_user)
            db.session.commit()
            ### 5) Retrieve new user to send to front
            u = user_schema.dump(new_user)

        except Exception as e:
            db.session.rollback()
            logging.warning(e)
            abort(500, "Erreur serveur, le compte n'as pas été créé")
        else:
            return make_response(jsonify({
                "status": "success",
                "message": "utilisateur créé avec succès",
                "user": u
            }), 201)
