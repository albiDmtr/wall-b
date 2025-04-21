# script to calibrate the intrinsic parameters of the camera
import cv2
import numpy as np
import glob
import os
import json

def calibrate_camera(images, pattern_size=(8, 6), square_size=25.0):
    # Prepare object points
    objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2) * square_size

    # Arrays to store object points and image points
    objpoints = []  # 3D points in real world space
    imgpoints = []  # 2D points in image plane

    for img in images:
        # Find chessboard corners
        ret, corners = cv2.findChessboardCorners(img, pattern_size, None)

        if ret:
            objpoints.append(objp)
            
            # Refine corner detection
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            corners2 = cv2.cornerSubPix(img, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

    # Calibrate camera
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img.shape[::-1], None, None)
    
    return ret, mtx, dist, rvecs, tvecs

def main():

    if not os.path.exists('calibration_images'):
        os.makedirs('calibration_images')
        print("Please place your stereo calibration images in the 'calibration_images' folder")
        return

    # Get all stereo images
    stereo_images = glob.glob('calibration_images/*.jpg')
    if not stereo_images:
        print("No calibration images found in 'calibration_images' folder")
        return

    # Arrays to store left and right images
    left_images = []
    right_images = []

    # Process each stereo image
    for stereo_img_path in stereo_images:
        # Read stereo image
        stereo_img = cv2.imread(stereo_img_path)
        if stereo_img is None:
            print(f"Could not read image: {stereo_img_path}")
            continue

        # Split into left and right images
        height, width = stereo_img.shape[:2]
        left_img = stereo_img[:, :width//2]
        right_img = stereo_img[:, width//2:]

        # Convert to grayscale
        left_gray = cv2.cvtColor(left_img, cv2.COLOR_BGR2GRAY)
        right_gray = cv2.cvtColor(right_img, cv2.COLOR_BGR2GRAY)

        left_images.append(left_gray)
        right_images.append(right_gray)

    # Calibrate left camera
    print("Calibrating left camera...")
    ret_left, mtx_left, dist_left, rvecs_left, tvecs_left = calibrate_camera(left_images)
    
    # Calibrate right camera
    print("Calibrating right camera...")
    ret_right, mtx_right, dist_right, rvecs_right, tvecs_right = calibrate_camera(right_images)

    # Save calibration results
    calibration_data = {
        'left_camera': {
            'matrix': mtx_left.tolist(),
            'distortion': dist_left.tolist()
        },
        'right_camera': {
            'matrix': mtx_right.tolist(),
            'distortion': dist_right.tolist()
        }
    }

    # Save to JSON file with pretty formatting
    with open('camera_intrinsic.json', 'w') as f:
        json.dump(calibration_data, f, indent=4)

    print("Calibration completed successfully!")
    print("Results saved to 'camera_intrinsic.json'")

if __name__ == "__main__":
    main()

