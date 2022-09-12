import cv2
import numpy as np
from threading import Lock
import face_recognition
from services.base_camera import BaseCamera
from services.profile_validator import ProfileCSVHandler
from services.frame_handler import FrameHandler
from services.face_reco_handler import FaceRecognitionHandler


class SecurityStreamHandler(BaseCamera):

    def __init__(self, camera_src):
        if str(camera_src)[0].isdigit():
            # handle webcams
            self.src = int(camera_src)
        else:
            # handle ip cams
            self.src = camera_src
        self.video = cv2.VideoCapture(self.src)
        self.ret, self.frame = self.video.read()
        self.process_this_frame = True
        self.known_face = ProfileCSVHandler()
        self.known_face_names = np.array(self.known_face.data.name + ' ' + self.known_face.data.surname)
        self.known_face_encodings = self.known_face.data.encodings

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
                        fr_handler = FrameHandler(self.frame)
                        # resize frame
                        fr_handler.resize_frame()
                        # convert color to be readable by face_recognition algorithm
                        fr_handler.convert_frame()
                        # search for faces inside the frame
                        face_reco = FaceRecognitionHandler(fr_handler.frame, self.known_face_encodings, self.known_face_names)
                        face_reco.locate_faces()
                        # if there is at least one located face
                        if len(face_reco.face_locations) > 0:
                            # if there is no face encoded already
                            if len(face_reco.face_encodings) < 1:
                                # encode faces
                                face_reco.encode_faces()
                                # face_reco.compare_face()
                                print(type(face_reco.known_face_encodings[0]))

                        for (top, right, bottom, left) in face_reco.face_locations:
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
