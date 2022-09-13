import csv
import os
import time
import json
import cv2
from flask import jsonify
import face_recognition
import pandas as pd
import numpy as np
from models.profile_model import Profile
from schemas.profile_schema import profiles_schema

my_json = {
    "id": 32,
    "account_id": 1,
    "name": "milliat",
    "validated": 2,
    "surname": "emmanuelle",
    "encodings": [-0.07509941,  0.09966819,  0.07738455, -0.09642928, -0.18945418,
        0.01215649, -0.02239991, -0.05916007,  0.21017282, -0.01903518,
        0.26672804,  0.03510177, -0.24539176,  0.04913574, -0.04691654,
        0.08022714, -0.12994431, -0.05488232, -0.08392768, -0.11044858,
        0.03674962,  0.10395939, -0.02759009, -0.00555113, -0.10092813,
       -0.37627861, -0.07315867, -0.02385227,  0.07160784, -0.12873805,
        0.0710662 ,  0.10401089, -0.11698695, -0.10150075,  0.06381802,
        0.0614795 , -0.03336444, -0.05638632,  0.14039497,  0.0771363 ,
       -0.11008338,  0.07202417,  0.04400693,  0.35079047,  0.14478807,
        0.06070555,  0.06939472, -0.05129296,  0.10653394, -0.32869241,
        0.11267324,  0.09945321,  0.12838605,  0.02314223,  0.14007574,
       -0.13222076, -0.04644953,  0.1285325 , -0.21347778,  0.18600166,
        0.14856228, -0.06232495, -0.06187056, -0.13201049,  0.20051761,
        0.11778794, -0.15525225, -0.07574394,  0.08729832, -0.12434323,
       -0.11205506,  0.00893894, -0.10380301, -0.15796264, -0.26634046,
        0.12470496,  0.44940594,  0.16090104, -0.22247496, -0.04062485,
       -0.03691912,  0.0350282 ,  0.04650059,  0.03413529, -0.06712194,
       -0.06547642, -0.05934014,  0.0218011 ,  0.20528705,  0.01993666,
       -0.07787866,  0.30743089,  0.02098749,  0.04008951,  0.02034467,
        0.08375082, -0.09949448, -0.07018872, -0.11354105, -0.00857642,
        0.03814591, -0.11354536,  0.01025195,  0.09257237, -0.20284757,
        0.21102493, -0.044951  ,  0.00577252,  0.04196067,  0.0200013 ,
       -0.09998182, -0.0169097 ,  0.20915614, -0.29209873,  0.20520115,
        0.19811693,  0.05810759,  0.15649098,  0.03360184,  0.01021523,
        0.06057822,  0.00485518, -0.05300514, -0.1390626 , -0.0289612 ,
       -0.07420611, -0.01771721,  0.04625626],
    "dob": "16/02/1918",
    "val_num": 1
}

ROOT_DIR = os.path.abspath(os.curdir)
DATA_FILE_PATH = ROOT_DIR + '/data/known_face_encodings.json'


class FrameHandler:

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

    def save_to_folder(self, account_id):
        # check if folder exists, otherwise create
        path = self.folder + account_id
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
        # save image within the frames/<id> folder with a filename as name_surname_unix time
        filename = f"/unknown_{int(time.time())}.jpg"
        cv2.imwrite(path + filename, self.frame)
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

