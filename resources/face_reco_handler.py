import face_recognition
import time
import os
import cv2
import numpy as np
from flask import make_response, jsonify
from flask_restful import Resource
from models.profile_model import Profile
from schemas.profile_schema import profiles_schema, profile_schema


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class FrameHandler(Resource):

    def __init__(self, frame):
        self.frame = frame
        self.folder = ROOT_DIR + '/frames/'

    def resize_frame(self):
        # Resizes frame to 1/4 of its size
        self.frame = cv2.resize(self.frame, (0, 0), fx=.25, fy=.25)
        return self.frame

    def convert_frame(self):
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses) or reverse
        self.frame = self.frame[:, :, ::-1]
        return self.frame

    def save_to_folder(self, profile_infos, ext):
        # save image with a filename as id_name_surname_unix time
        filename = f"{profile_infos['id']}_{profile_infos['name']}_{profile_infos['surname']}_{int(time.time())}.{ext}"
        cv2.imwrite(self.folder + filename, self.frame)
        return


class FaceRecognitionHandler(Resource):

    def __init__(self, frame, known_face_encodings, known_face_names):
        self.frame_handler = FrameHandler(frame)
        self.frame = self.frame_handler.frame
        self.face_encodings = []
        self.known_face_encodings = known_face_encodings
        self.face_name = "unknown"
        self.known_face_names = known_face_names

    def _locate_and_encode_face(self):
        self.face_locations = face_recognition.face_locations(self.frame)
        if len(self.face_locations) < 1:
            return
        self.face_encodings = face_recognition.face_encodings(self.frame, self.face_locations)
        # return only the first face if multiple faces are on the frame
        return

    def _compare_face(self):
        """

        :return:
        """
        """
        1) Compare the euclidean distance ratio to validate that one located face match with known faces (0.6 means faces match)
        """
        matches = face_recognition.compare_faces(self.known_face_encodings, self.face_encodings[0])
        """
        2) Compare the matches to see which one has the closest distance
        """
        face_distances = face_recognition.face_distance(self.known_face_encodings, self.face_encodings[0])
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            self.face_name = self.known_face_names[best_match_index]

    def get_frame_comparison(self):
        """

        :return:
        """
        """
        1) RESIZE FRAME
        """
        self.frame_handler.resize_frame()
        """
        2) CONVERT COLOR
        """
        self.frame_handler.convert_frame()
        """
        3) LOCATE FACES AND ENCODE FACE FROM FRAME
        """
        self._locate_and_encode_face()
        """
        4) FINALLY COMPARE THE ENCODED FACE TO KNOWN FACE ENCODINGS AND RETURN RESULT
        """
        self._compare_face()
