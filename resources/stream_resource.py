import cv2
from threading import Lock
from flask import Response, request
from services.base_camera import BaseCamera

STREAM_ENDPOINT = '/cam-api/v1/stream'


class StreamResource(BaseCamera):

    def __init__(self, camera_src):
        if str(camera_src)[0].isdigit():
            self.src = int(camera_src)
        else:
            self.src = camera_src
        self.video = cv2.VideoCapture(self.src)
        self.ret, self.frame = self.video.read()

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

                # encode the frame in JPEG format
                ret, jpeg = cv2.imencode('.jpg', self.frame)
                # ensure the frame was successfully encoded
                if not self.ret:
                    continue

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

                if cv2.waitKey(1) == ord('q'):
                    break
