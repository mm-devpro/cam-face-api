import logging
from flask_restful import Resource
from flask import request, abort, jsonify, g, make_response
from database import db
from models.user_model import User
from schemas.user_schema import users_schema, user_schema
from services.variables import USER_VALIDATED_GET_ARGS, USER_VALIDATED_ARGS
from services.auth import is_admin

USER_ENDPOINT = '/cam-api/v1/user'


class UserResource(Resource):

    def __init__(self):
        self._admin_val = is_admin(g, ['admin', 'super-admin'])
        self._super_admin_val = is_admin(g, ['super-admin'])
        self._curr_account = g.cookie['user']['account']

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
        users = User.query.filter_by(account_id=self._curr_account, **data).all()
        return users

    def _get_by_id(self, user_id):
        # Get User for the current account
        user = User.query.filter_by(account_id=self._curr_account, id=user_id).first()
        return user

    def post(self):
        json_data = request.get_json()
        if not json_data:
            abort(401, "data should be in json")
        try:
            # only (super)admin can create new user
            if self._admin_val is False:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Accès non authorisé",
                }), 403)
            # field validation (removing potential bad fields from request)
            val_data = {k: v for (k, v) in json_data.items() if k in USER_VALIDATED_ARGS}
            # load new user
            new_user = user_schema.load(val_data, session=db.session)
            # add new user to db
            db.session.add(new_user)
            # link new user to current account
            new_user.account_id = self._curr_account

            db.session.commit()
            # get new user infos to send to front
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

    def put(self, user_id=None):
        json_data = request.get_json()
        if not json_data:
            abort(401, "data should be in json")

        try:
            # validate data
            val_data = {k: v for (k, v) in json_data.items() if k in USER_VALIDATED_ARGS}
            # retrieve user to update

            if user_id is not None:
                """
                RETRIEVE ANOTHER USER THAN CURRENT
                """
                # retrieve user with id
                user = self._get_by_id(user_id)

                if user.account_id != self._curr_account:
                    """
                    OUTSIDE OF THE ACCOUNT SCOPE
                    """
                    # you must be super-admin
                    if self._super_admin_val is False:
                        return make_response(jsonify({
                            "status": "error",
                            "message": "Accès non authorisé",
                        }), 403)
                else:
                    """
                    INSIDE THE ACCOUNT SCOPE
                    """
                    # you must be at least admin
                    if self._admin_val is False:
                        return make_response(jsonify({
                            "status": "error",
                            "message": "Accès non authorisé",
                        }), 403)
            else:
                """
                RETRIEVE CURRENT USER
                """
                user = self._get_by_id(g.cookie['id'])

            # update user with new values
            for k, v in val_data.items():
                setattr(user, k, v)
            db.session.commit()

            # dump user to send it to front
            u = user_schema.dump(user)

        except Exception as e:
            db.session.rollback()
            logging.warning(e)
            abort(403, f"Probleme pour actualiser l'utilisateur: {e}")
        else:
            return make_response(jsonify({
                "status": "success",
                "message": "utilisateur modifié avec succès",
                "user": u
            }), 200)

    def delete(self, user_id=None):
        try:
            # Validate current user to be at least admin to allow access
            if self._admin_val is False:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Accès non authorisé",
                }), 403)
            # retrieve user
            if user_id is not None:
                acc_to_del = self._get_by_id(user_id)
            else:
                acc_to_del = self._get_by_id(g.cookie["id"])
            # check if user exists
            if acc_to_del is None:
                abort(403, "Pas de compte correspondant à l'id")
            # Validate that user is in Account Scope
            elif acc_to_del.account_id != self._curr_account:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Accès non authorisé",
                }), 403)
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
                "message": "utilisateur supprimé avec succès",
            }), 200)

