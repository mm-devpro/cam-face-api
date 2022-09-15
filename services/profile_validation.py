import os
import time
import json
import cv2
import face_recognition
import pandas as pd
import numpy as np
from models.profile_model import Profile
from schemas.profile_schema import profiles_schema

ROOT_DIR = os.path.abspath(os.curdir)
DATA_FILE_PATH = ROOT_DIR + '/data/known_face_encodings.json'


class FrameHandler:

    def __init__(self, frame):
        self.original_frame = frame
        self.retouched_frame = frame
        self.folder = ROOT_DIR + '/data/frames/'

    def resize_frame(self):
        # Resizes frame to 1/4 of its size
        self.retouched_frame = cv2.resize(self.retouched_frame, (0, 0), fx=.25, fy=.25)
        return self.retouched_frame

    def convert_BGR2RGB(self):
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        self.retouched_frame = cv2.cvtColor(self.retouched_frame, cv2.COLOR_BGR2RGB)
        return self.retouched_frame

    def convert_RGB2BGR(self):
        # Convert the image from RGB color (which face_recognition uses) to BGR color (which OpenCV uses)
        self.retouched_frame = cv2.cvtColor(self.retouched_frame, cv2.COLOR_RGB2BGR)
        return self.retouched_frame

    def save_to_folder(self, account_id):
        # check if folder exists, otherwise create
        path = self.folder + str(account_id)
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
        # save image within the frames/<id> folder with a filename as name_surname_unix time
        filename = f"/unknown_{int(time.time())}.jpg"
        cv2.imwrite(path + filename, self.original_frame)
        return


class KnownFacesJSONHandler:

    def __init__(self):
        with open(DATA_FILE_PATH, "r") as f:
            self.data = pd.DataFrame(json.load(f))

    def reload_file(self):
        pr = Profile.query.all()
        if pr is not None:
            pr_sch = profiles_schema.dumps(pr)

        with open(DATA_FILE_PATH, 'w') as f:
            f.write(pr_sch)


class ProfileValidator:

    def __init__(self, frame, known_face_encodings, known_face_ids):
        self.frame = frame
        self.known_face_encodings = known_face_encodings
        self.known_face_ids = known_face_ids
        self.face_locations = []
        self.face_encodings = []
        self.face_id = 0

    def locate_faces(self):
        self.face_locations = face_recognition.face_locations(self.frame)
        return self.face_locations

    def encode_faces(self):
        self.face_encodings = face_recognition.face_encodings(self.frame, self.face_locations)
        return self.face_encodings

    def compare_face(self):
        """

        :return:
        """
        """
        1)  Compare the euclidean distance ratio to validate that at least 
            one located face match with known faces (0.6 means faces match)
        """
        matches = face_recognition.compare_faces(self.known_face_encodings, self.face_encodings[0])
        """
        2) Compare the matches to see which one has the closest distance
        """
        face_distances = face_recognition.face_distance(self.known_face_encodings, self.face_encodings[0])
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            self.face_id = self.known_face_ids[best_match_index]
            return self.face_id

