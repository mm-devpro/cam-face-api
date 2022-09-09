import cv2
from threading import Lock
import face_recognition
from database import db
from models.profile_model import Profile
from services.base_camera import BaseCamera
from resources.face_reco_handler import FaceRecognitionHandler


class StreamHandler(BaseCamera):

    def __init__(self, camera_src, known_face_encodings=[], known_face_names=[]):
        if str(camera_src)[0].isdigit():
            self.src = int(camera_src)
        else:
            self.src = camera_src
        self.video = cv2.VideoCapture(self.src)
        self.ret, self.frame = self.video.read()
        self.process_this_frame = True
        self.known_face_encodings = known_face_encodings
        self.known_face_names = known_face_names
        self.face_encodings = []

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

                if self.frame is not None:
                    # Only process every other frame of video to save time
                    if self.process_this_frame:
                        small_frame = cv2.resize(self.frame, (0, 0), fx=0.25, fy=0.25)
                        rgb_small_frame = small_frame[:, :, ::-1]
                        face_locations = face_recognition.face_locations(rgb_small_frame)
                        if len(face_locations) > 0:
                            if len(self.face_encodings) < 1:
                                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                                print(self.face_encodings)
                            for (top, right, bottom, left) in face_locations:
                                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                                top *= 4
                                right *= 4
                                bottom *= 4
                                left *= 4

                                # Draw a box around the face
                                cv2.rectangle(self.frame, (left, top), (right, bottom), (0, 0, 255), 2)

                        # profiles = Profile.query.all()
                        # face_reco_handler = FaceRecognitionHandler(self.frame, self.known_face_encodings, self.known_face_names)
                        # face_reco_handler.get_frame_comparison()

                self.process_this_frame = not self.process_this_frame

                # encode the frame in JPEG format
                ret, jpeg = cv2.imencode('.jpg', self.frame)
                # ensure the frame was successfully encoded
                if not self.ret:
                    continue

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

                if cv2.waitKey(1) == ord('q'):
                    break
