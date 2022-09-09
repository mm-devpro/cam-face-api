import logging
from flask_restful import Resource
from flask import request, abort, jsonify, g, make_response, Response
from database import db
from models.camera_model import Camera
from models.profile_model import Profile
from schemas.camera_schema import cameras_schema, camera_schema
from resources.stream_handler import StreamHandler
from services.variables import CAMERA_VALIDATED_GET_ARGS, CAMERA_VALIDATED_ARGS
from services.auth import is_admin

CAMERA_ENDPOINT = '/cam-api/v1/camera'
STREAM_ENDPOINT = '/cam-api/v1/stream'


class CameraResource(Resource):

    def __init__(self):
        self._admin_val = is_admin(g, ['admin', 'super-admin'])
        self._super_admin_val = is_admin(g, ['super-admin'])
        self._curr_account = g.cookie['user']['account']

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
        cameras = Camera.query.filter_by(account_id=self._curr_account, **data).all()
        return cameras

    def _get_by_id(self, camera_id):
        # Get Camera from current account
        camera = Camera.query.filter_by(account_id=self._curr_account, id=camera_id).first()
        return camera

    def post(self):
        json_data = request.get_json()
        if not json_data:
            abort(401, "data should be in json")
        try:
            # Must be at least admin to post a camera
            if self._admin_val is False:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Accès non authorisé",
                }), 403)
            # validate data
            val_data = {k: v for (k, v) in json_data.items() if k in CAMERA_VALIDATED_ARGS}
            # create new camera
            new_camera = camera_schema.load(val_data, session=db.session)
            # add to database
            db.session.add(new_camera)
            # link camera to current account
            new_camera.account_id = self._curr_account
            db.session.commit()
            # retrieve new camera to send to front
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

    def put(self, camera_id):
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
            val_data = {k: v for (k, v) in json_data.items() if k in CAMERA_VALIDATED_ARGS}
            # retrieve camera
            camera = self._get_by_id(camera_id)
            # check if camera exists
            if camera is None:
                abort(404, f"Pas de camera correspondant")
            # validate that camera is from the same account as current to allow update
            elif camera.account_id != self._curr_account:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Accès non authorisé",
                }), 403)
            else:
                # update data
                for k, v in val_data.items():
                    setattr(camera, k, v)
                db.session.commit()

            # dump new camera to send to front
            cam = camera_schema.dump(camera)
        except Exception as e:
            db.session.rollback()
            logging.warning(e)
            abort(403, f"Probleme pour actualiser la camera: {e}")
        else:
            return make_response(jsonify({
                "status": "success",
                "message": "camera modifié avec succès",
                "camera": cam
            }), 200)

    def delete(self, camera_id):
        try:
            # Validate current user to be at least admin to allow access
            if self._admin_val is False:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Accès non authorisé",
                }), 403)
            # retrieve camera
            cam_to_del = self._get_by_id(camera_id)
            # check if camera exists
            if cam_to_del is None:
                abort(404, f"Pas de camera correspondant")
            # validate that camera is from the same account as current to allow deletion
            elif cam_to_del.account_id != self._curr_account:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Accès non authorisé",
                }), 403)
            else:
                db.session.delete(cam_to_del)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.warning(e)
            abort(403, f"Probleme pour actualiser la camera: {e}")
        else:
            return make_response(jsonify({
                "status": "success",
                "message": "camera supprimé avec succès",
            }), 200)


class StreamResource (Resource):

    def get(self):
        source = request.args.get("source")
        # profiles = Profile.query.all()
        # known_face_encodings = [profile.face_encoding for profile in profiles]
        # known_face_names = [profile.name for profile in profiles]
        # app.app_context().push()
        camera = StreamHandler(source)
        return Response(camera.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
