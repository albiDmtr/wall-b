import numpy as np
import cv2
import glob
import os
import json

# camera intrinsic parameters
left_camera_matrix= np.array([
    [982.6092245580564, 0.0, 634.4875499001336],
    [0.0, 980.6961415333275, 360.76769051716457],
    [0.0, 0.0, 1.0]
])
left_distortion = np.array([
    -0.5553273388834578,
    0.46623843458720193,
    0.0017533758427258099,
    -0.0012195212670231615,
    -0.2490172142747216
])

right_camera_matrix = np.array([
    [989.4622526566694, 0.0, 613.55919957331],
    [0.0, 989.8249071672162, 335.6721285759285],
    [0.0, 0.0, 1.0]
])
right_distortion = np.array([
    -0.5172544193761841,
    0.3436908271415489,
    0.001095094351449141,
    0.007036740613665229,
    -0.1014769554729703
])

# Checkerboard parameters
CHECKERBOARD = (8, 6)  # Number of inner corners (vertices)
SQUARE_SIZE = 25  # mm

def main():
    # Prepare object points
    objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2) * SQUARE_SIZE

    # Arrays to store object points and image points from all images
    objpoints = []  # 3D points in real world space
    left_imgpoints = []  # 2D points in left image plane
    right_imgpoints = []  # 2D points in right image plane

    # Get list of calibration images
    images = glob.glob('./calibration_images/*.jpg')
    print(f"Found {len(images)} calibration images")

    for img_path in images:
        # Read and split the stereo image
        img = cv2.imread(img_path)
        if img is None:
            print(f"Failed to load image: {img_path}")
            continue

        # Split into left and right images
        height, width = img.shape[:2]
        left_img = img[:, :width//2]
        right_img = img[:, width//2:]

        # Convert to grayscale
        left_gray = cv2.cvtColor(left_img, cv2.COLOR_BGR2GRAY)
        right_gray = cv2.cvtColor(right_img, cv2.COLOR_BGR2GRAY)

        # Find chessboard corners
        left_ret, left_corners = cv2.findChessboardCorners(left_gray, CHECKERBOARD, None)
        right_ret, right_corners = cv2.findChessboardCorners(right_gray, CHECKERBOARD, None)

        if left_ret and right_ret:
            # Refine corner detection
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            left_corners2 = cv2.cornerSubPix(left_gray, left_corners, (11, 11), (-1, -1), criteria)
            right_corners2 = cv2.cornerSubPix(right_gray, right_corners, (11, 11), (-1, -1), criteria)

            # Add points to lists
            objpoints.append(objp)
            left_imgpoints.append(left_corners2)
            right_imgpoints.append(right_corners2)

            # Draw and display the corners
            cv2.drawChessboardCorners(left_img, CHECKERBOARD, left_corners2, left_ret)
            cv2.drawChessboardCorners(right_img, CHECKERBOARD, right_corners2, right_ret)
            
            # Combine images for display
            display_img = np.hstack((left_img, right_img))
            cv2.imshow('Stereo Calibration', display_img)
            cv2.waitKey(500)  # Display for 500ms

    cv2.destroyAllWindows()

    if len(objpoints) < 3:
        print("Not enough valid calibration images found. Need at least 3 images with detected corners.")
        return

    print(f"Using {len(objpoints)} valid calibration images")

    # Perform stereo calibration
    ret, _, _, _, _, R, T, E, F = cv2.stereoCalibrate(
        objpoints, left_imgpoints, right_imgpoints,
        left_camera_matrix, left_distortion,
        right_camera_matrix, right_distortion,
        (left_gray.shape[1], left_gray.shape[0]),
        flags=cv2.CALIB_FIX_INTRINSIC
    )

    if ret:
        print("\nStereo Calibration Results:")
        print(f"Reprojection Error: {ret}")
        print("\nRotation Matrix (R):")
        print(R)
        print("\nTranslation Vector (T):")
        print(T)
        print("\nEssential Matrix (E):")
        print(E)
        print("\nFundamental Matrix (F):")
        print(F)

        # Convert numpy arrays to lists for JSON serialization
        calibration_data = {
            "reprojection_error": float(ret),
            "R": R.tolist(),
            "T": T.tolist(),
            "E": E.tolist(),
            "F": F.tolist(),
            "left_camera_matrix": left_camera_matrix.tolist(),
            "right_camera_matrix": right_camera_matrix.tolist(),
            "left_distortion": left_distortion.tolist(),
            "right_distortion": right_distortion.tolist()
        }

        # Save the results to JSON
        with open('camera_calibration.json', 'w') as f:
            json.dump(calibration_data, f, indent=4)
        print("\nCalibration results saved to 'camera_calibration.json'")
    else:
        print("Stereo calibration failed!")

if __name__ == "__main__":
    main()

