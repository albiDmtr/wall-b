from cam.stereo_processing import undistort_rectify, save_to_desktop, visualize_disparity
from cam.stereo_cam import stereo_cam
import numpy as np
import cv2
import time

if __name__ == "__main__":

    # Initialize the stereo camera
    camera = stereo_cam()
    camera.start()
    
    frame = camera.capture()
    save_to_desktop(frame)

    left, right = undistort_rectify(frame)
    disparity_map = visualize_disparity(left, right)
    save_to_desktop(disparity_map)



    # clean up
    camera.stop()
