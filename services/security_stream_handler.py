import time
import cv2
from ast import literal_eval
import numpy as np
from threading import Lock
import face_recognition
from flask import g
from flask_restful import Resource
from services.base_camera import BaseCamera
from services.profile_validation import KnownFacesJSONHandler, FrameHandler, ProfileValidator
from models.profile_model import Profile


class StreamHandler(BaseCamera, Resource):

    def __init__(self, camera_src):
        if str(camera_src)[0].isdigit():
            # handle webcams
            self.src = int(camera_src)
        else:
            # handle ip cams
            self.src = camera_src
        self.video = cv2.VideoCapture(self.src)
        self.ret, self.frame = self.video.read()
        self.process_this_frame = 1
        self.known_faces = KnownFacesJSONHandler().data
        self.known_face_ids = list(self.known_faces.loc[:, "id"])
        self.known_face_encodings = [literal_eval(x) for x in self.known_faces.loc[:, "encodings"]]
        self.face_id = int(0)
        self.face_validator = int(0)
        self.face_unknown = int(0)
        self.validated = False

    def __del__(self):
        self.video.release()

    def gen_frames(self):
        lock = Lock()

        # check if camera is opened
        if self.video.isOpened():
            self.ret, self.frame = self.video.read()
        else:
            self.ret = False

        while self.ret:
            with lock:
                self.ret, self.frame = self.video.read()

                if self.frame is None:
                    continue
                else:
                    self.process_this_frame += 1
                    # Only process every 10 frames
                    if self.process_this_frame == 10:
                        """
                        1) Handle Frame
                        """
                        fr_handler = FrameHandler(self.frame)
                        # resize frame
                        fr_handler.resize_frame()
                        # convert color to be readable by face_recognition algorithm
                        fr_handler.convert_BGR2RGB()
                        """
                        2) locate and reckon faces
                        """
                        face_reco = ProfileValidator(fr_handler.retouched_frame, self.known_face_encodings, self.known_face_ids)
                        face_reco.locate_faces()
                        # if there is at least one located face
                        if len(face_reco.face_locations) > 0:
                            # encode faces
                            face_reco.encode_faces()
                            profile_id = face_reco.compare_face()
                            # profile validator
                            if profile_id is not None:
                                if self.face_validator == 0:
                                    self.face_id = profile_id
                                    self.face_validator += 1
                                elif 0 < self.face_validator < 5:
                                    if self.face_id == profile_id:
                                        self.face_validator += 1
                                    else:
                                        self.face_id = profile_id
                                        self.face_validator = 1
                                elif self.face_validator >= 5:
                                    self.validated = True
                            else:
                                self.face_unknown += 1
                                # wait for 10 processes of unknown faces to store it into frames/account_id folder
                                if self.face_unknown == 10:
                                    fr_handler.save_to_folder(3)
                                    self.face_unknown = 0
                        self.process_this_frame = 1

                        for (top, right, bottom, left) in face_reco.face_locations:
                            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                            top *= 4
                            right *= 4
                            bottom *= 4
                            left *= 4

                            # Draw a box around the face
                            cv2.rectangle(self.frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # encode the frame in JPEG format
                ret, jpeg = cv2.imencode('.jpg', self.frame)
                # ensure the frame was successfully encoded
                if not self.ret:
                    continue

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

                if cv2.waitKey(1) == ord('q'):
                    break