import logging
from flask_restful import Resource
from flask import request, abort, jsonify, g, make_response
from database import db
from models.camera_model import Camera
from schemas.camera_schema import cameras_schema, camera_schema
from services.variables import CAMERA_VALIDATED_GET_ARGS

CAMERA_ENDPOINT = '/cam-api/v1/camera'


class CameraResource(Resource):

    def get(self, camera_id=None):
        try:
            if not camera_id:
                args = {arg: request.args.get(arg) for arg in request.args if arg in CAMERA_VALIDATED_GET_ARGS}
                cameras = self._get_all(args)
                dumped = cameras_schema.dump(cameras)
            else:
                camera = self._get_by_id(camera_id)
                dumped = camera_schema.dump(camera)

            if not dumped:
                abort(400)

        except Exception as e:
            logging.warning(e)
            abort(400, "pas de camera correspondante")
        else:
            return make_response(jsonify({
                "status": "success",
                "message": "Camera(s) récupéré(s)",
                "camera": dumped,
                "result": len(dumped)
            }), 200)

    def _get_all(self, data=None):
        # Get Cameras from current account
        cameras = Camera.query.filter_by(account_id=g.cookie['user']['account'], **data).all()
        return cameras

    def _get_by_id(self, camera_id):
        # Get Camera from current account
        camera = Camera.query.filter_by(account_id=g.cookie['user']['account'], id=camera_id).first()
        return camera

    def post(self):
        json_data = request.get_json()
        if not json_data:
            abort(401, "data should be in json")
        try:
            ### validate data
            val_camera = camera_schema.dump(json_data)
            ### create new camera
            new_camera = camera_schema.load(val_camera, session=db.session)
            ### add to database
            db.session.add(new_camera)
            ### link camera to current account
            new_camera.account_id = g.cookie['user']['account']
            db.session.commit()
            ### retrieve new camera to send to front
            cam = camera_schema.dump(new_camera)

        except Exception as e:
            db.session.rollback()
            logging.warning(e)
            abort(403, "Cette caméra est deja existante")
        else:
            return make_response(jsonify({
                "status": "success",
                "message": "caméra créée avec succès",
                "camera": cam
            }), 201)

    def put(self):
        pass

    def __del__(self):
        pass

