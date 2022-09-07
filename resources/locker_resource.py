import logging
from flask_restful import Resource
from flask import request, abort, jsonify, g, make_response
from database import db
from models.locker_model import Locker
from schemas.locker_schema import lockers_schema, locker_schema
from services.variables import LOCKER_VALIDATED_GET_ARGS

LOCKER_ENDPOINT = '/cam-api/v1/locker'


class LockerResource(Resource):

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
            abort(400, "pas de compte correspondant")
        else:
            return make_response(jsonify({
                "status": "success",
                "message": "locker(s) récupéré(s)",
                "locker": dumped,
                "result": len(dumped)
            }), 200)

    def _get_all(self, data=None):
        if data:
            lockers = Locker.query.filter_by(**data).all()
        else:
            lockers = Locker.query.all()
        return lockers

    def _get_by_id(self, locker_id):
        locker = Locker.query.filter_by(id=locker_id).first()
        return locker

    def post(self):
        json_data = request.get_json()
        if not json_data:
            abort(401, "data should be in json")
        try:
            ### validate data
            val_locker = locker_schema.dump(json_data)
            ### create new locker
            new_locker = locker_schema.load(val_locker, session=db.session)
            ### add to database
            db.session.add(new_locker)
            db.session.commit()
            ### retrieve new locker to send to front
            lo = locker_schema.dump(new_locker)

        except Exception as e:
            db.session.rollback()
            logging.warning(e)
            abort(403, "Ce compte est deja existant")
        else:
            return make_response(jsonify({
                "status": "success",
                "message": "compte créé avec succès",
                "locker": lo
            }), 201)

    def put(self):
        pass

    def __del__(self):
        pass

