from cam.capture import disparity_to_m
import numpy as np
import cv2
import time

if __name__ == "__main__":
    print(disparity_to_m(42.5))
    print(disparity_to_m(65))