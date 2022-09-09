import cv2
from threading import Lock
from flask import Response, request
from services.base_camera import BaseCamera
from resources.face_reco_handler import FaceRecognitionHandler

STREAM_ENDPOINT = '/cam-api/v1/stream'


class StreamHandler(BaseCamera):

    def __init__(self, camera_src):
        if str(camera_src)[0].isdigit():
            self.src = int(camera_src)
        else:
            self.src = camera_src
        self.video = cv2.VideoCapture(self.src)
        self.ret, self.frame = self.video.read()
        self.process_this_frame = True

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
                        face_reco_handler = FaceRecognitionHandler(self.frame)
                        face_reco_handler.get_frame_comparison()

                        print(f"face_reco : \n {face_reco_handler.known_face_encodings}"
                              f"\n {face_reco_handler.known_face_names}"
                              f"\n {face_reco_handler.face_encodings}"
                              f"\n {face_reco_handler.face_name}")

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
