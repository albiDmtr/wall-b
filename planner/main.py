from cam.stereo_processing import undistort_rectify, save_to_desktop, visualize_disparity
from cam.stereo_cam import stereo_cam
import numpy as np
import cv2
import time
from ws_client import run_client
from listen.listener import listener

#run_client()

lis = listener()

start_time = time.time()
print(lis.listen())
end_time = time.time()

print("Time taken to run listener:", time.time() - start_time)

