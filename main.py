import cv2

import numpy as np

import time

import cv2.ximgproc as ximgproc

# Left camera intrinsic parameters, such as focal length
left_camera_matrix = np.array([
    [2036.5, 1.3, 583.4],
    [0, 2028.6, 449.5],
    [0, 0, 1]
])

right_camera_matrix = np.array([
    [2036.5, 1.3, 583.4],
    [0, 2028.6, 449.5],
    [0, 0, 1]
])

# Distortion coefficients, K1, K2, K3 for radial distortion, P1, P2 for tangential distortion
left_distortion = np.array([[-0.3863, 0.5091, -0.0011, 0.001, -2.6353]])
right_distortion = np.array([[-0.4256, 1.5578, -0.0023, 0.0005, -11.6757]])

# Rotation matrix
R = np.array([
    [0.9999, 0.0012, 0.0164],
    [-0.0011, 1, -0.0019],
    [-0.0164, 0.0019, 0.9999]
])

# Translation matrix
T = np.array([[-85.9802], [0.0723], [1.1451]])

def run(source, width, height):
    # Initialize SGBM parameters
    size = (width // 2, height)
    R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(left_camera_matrix, left_distortion,
                                                                    right_camera_matrix, right_distortion, size, R,
                                                                    T)

    # Create rectification mapping tables to map points between original and rectified images
    left_map1, left_map2 = cv2.initUndistortRectifyMap(left_camera_matrix, left_distortion, R1, P1, size, cv2.CV_16SC2)
    right_map1, right_map2 = cv2.initUndistortRectifyMap(right_camera_matrix, right_distortion, R2, P2, size, cv2.CV_16SC2)

    # Load video file
    capture = cv2.VideoCapture(source)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)   # Set frame width and height
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    WIN_NAME = 'Deep disp'

    # Read video
    fps = 0.0

    ret, frame = capture.read()
    while ret:
        # Start timer
        t1 = time.time()
        # Check if frame was read successfully
        ret, frame = capture.read()
        # Get frame dimensions
        width, height = frame.shape[1], frame.shape[0]
        
        # Split into left and right images
        frame1 = frame[0:height, 0:width // 2]
        frame2 = frame[0:height, width // 2:  width]
        
        # Convert BGR to grayscale for distortion correction
        imgL = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        imgR = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        # Remapping - placing pixels from one image to specified positions in another image
        # Reconstruct undistorted images based on MATLAB measurement data, input must be grayscale
        img1_rectified = cv2.remap(imgL, left_map1, left_map2, cv2.INTER_LINEAR)
        img2_rectified = cv2.remap(imgR, right_map1, right_map2, cv2.INTER_LINEAR)
        #cv2.imshow('Left Rectified', img1_rectified)
        # Convert to OpenCV BGR format
        imageL = cv2.cvtColor(img1_rectified, cv2.COLOR_GRAY2BGR)
        imageR = cv2.cvtColor(img2_rectified, cv2.COLOR_GRAY2BGR)

        radius = 8

        eps = 1000

        guided_filter = ximgproc.createGuidedFilter(guide=imageL, radius=radius, eps=eps)
        imgL = guided_filter.filter(imageL)
        imgR = guided_filter.filter(imageR)
        guided_filter = ximgproc.createGuidedFilter(guide=imageR, radius=radius, eps=eps)


        blockSize = 3
        
        img_channels = 3

        stereo = cv2.StereoSGBM_create(minDisparity=0,
                                    numDisparities=128,
                                    blockSize=blockSize,
                                    P1=8 * img_channels * blockSize * blockSize,
                                    P2=32 * img_channels * blockSize * blockSize,
                                    disp12MaxDiff=-1,
                                    preFilterCap=63,
                                    uniquenessRatio=10,
                                    speckleWindowSize=100,
                                    speckleRange=1,
                                    mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY)
        right_matcher = cv2.ximgproc.createRightMatcher(stereo)
        
        lmbda = 80000
        sigma = 3
        
        wls_filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=stereo)
        wls_filter.setLambda(lmbda)
        wls_filter.setSigmaColor(sigma)
        
        # Compute disparity map
        disparity_left = stereo.compute(imgL, imgR)
        disparity_right = right_matcher.compute(imgR, imgL)
        disparity_left = np.int16(disparity_left)
        disparity_right = np.int16(disparity_right)
        filteredImg = wls_filter.filter(disparity_left, imgL, imgR, disparity_right)
        mean = np.mean(filteredImg)
        std = np.std(filteredImg)
        
        filteredImg[filteredImg < mean - 2 * std] = mean
        filteredImg[filteredImg > mean + 2 * std] = mean
        
        # Normalize disparity map
        filteredImg = cv2.normalize(src=filteredImg, dst=filteredImg, beta=0, alpha=255, norm_type=cv2.NORM_MINMAX)
        filteredImg = np.uint8(filteredImg)
        
        ColorImg = cv2.applyColorMap(cv2.convertScaleAbs(filteredImg, alpha=1), cv2.COLORMAP_JET)
        
        # Display disparity map
        cv2.imshow('DisparityMap', filteredImg)
        cv2.imshow('ColorMap', ColorImg)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xff == ord('q'):
            break
    # Release resources
    capture.release()

    # Close all windows
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run(0, 2560, 720) 