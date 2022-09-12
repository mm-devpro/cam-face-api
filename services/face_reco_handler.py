import numpy as np
import face_recognition


class FaceRecognitionHandler:

    def __init__(self, frame, known_face_encodings, known_face_names):
        self.frame = frame
        self.known_face_encodings = known_face_encodings
        self.known_face_names = known_face_names
        self.face_locations = []
        self.face_encodings = []
        self.face_name = "unknown"

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
        1) Compare the euclidean distance ratio to validate that one located face match with known faces (0.6 means faces match)
        """
        matches = face_recognition.compare_faces(self.known_face_encodings, self.face_encodings[0])
        """
        2) Compare the matches to see which one has the closest distance
        """
        face_distances = face_recognition.face_distance([self.known_face_encodings], self.face_encodings[0])
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            self.face_name = self.known_face_names[best_match_index]
            return self.face_name


