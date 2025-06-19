import cv2
import numpy as np
import io
import time
from threading import Thread, Lock

class stereo_cam:
    def __init__(self, camera_index=0, resolution=(2560, 720)):
        self.camera_index = camera_index
        self.resolution = resolution
        self.cap = None
        self.stream = None
        self.thread = None
        self.frame = None
        self.stopped = False
        self.lock = Lock()

    def start(self):
        if self.cap is not None and self.cap.isOpened():
            print("Camera is already open.")
            return

        self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_V4L2)
        if not self.cap.isOpened():
            raise IOError(f"Cannot open camera {self.camera_index}")

        self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])

        self.stream = io.BytesIO()

        self.stopped = False
        self.thread = Thread(target=self._update, args=())
        self.thread.daemon = True
        self.thread.start()
        time.sleep(3)

    def _update(self):
        while not self.stopped:
            grabbed, frame = self.cap.read()
            if not grabbed:
                print("Camera disconnected or error occurred.  Stopping capture.")
                self.stop()
                return

            with self.lock:
                self.frame = frame
            
            time.sleep(0.01)
    
    def read(self):
        with self.lock:
            if self.frame is not None:
                return self.frame.copy()
            else:
                return None

    def stop(self):
        self.stopped = True
        if self.thread is not None:
            self.thread.join()
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        print("Camera stopped")

    def __del__(self):
        self.stop()

    def capture(self):
        frame = self.read()
        if frame is None:
            print("Error taking picture: No frame available.")
            return None
        return frame