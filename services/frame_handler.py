import os
import time
import cv2

ROOT_DIR = os.path.abspath(os.curdir)


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

    def save_to_folder(self, account_id, profile_infos, ext):
        # save image within the frames/<id> folder with a filename as name_surname_unix time
        filename = f"{account_id}/{profile_infos['name']}_{profile_infos['surname']}_{int(time.time())}.{ext}"
        cv2.imwrite(self.folder + filename, self.frame)
        return
