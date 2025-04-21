import cv2
import numpy as np

def undistort_and_remap(image, camera_matrix, distortion, R, P, size):
    """
    Corrects lens distortion and rectifies an image using camera parameters.
    
    Args:
        image: Input image to be rectified
        camera_matrix: Camera intrinsic matrix
        distortion: Distortion coefficients
        R: Rotation matrix
        P: Projection matrix
        size: Output image size
        
    Returns:
        Rectified image with corrected distortion
    """
    map1, map2 = cv2.initUndistortRectifyMap(camera_matrix, distortion, R, P, size, cv2.CV_32FC1)
    rectified_image = cv2.remap(image, map1, map2, cv2.INTER_CUBIC)
    return rectified_image


def cat2images(limg, rimg):
    """
    Concatenates left and right images side by side with a separator line.
    
    Args:
        limg: Left image
        rimg: Right image
        
    Returns:
        Combined image with both left and right images
    """
    HEIGHT = limg.shape[0]
    WIDTH = limg.shape[1]
    imgcat = np.zeros((HEIGHT, WIDTH * 2 + 20, 3))
    imgcat[:, :WIDTH, :] = limg
    imgcat[:, -WIDTH:, :] = rimg
    # Add horizontal separator lines every 32 pixels
    for i in range(int(HEIGHT / 32)):
        imgcat[i * 32, :, :] = 255
    return imgcat

# Read the input image and split it into left and right images
# The input image contains both left and right camera views side by side
img = cv2.imread("251.jpg")
left_image = img[0:720, 0:1280]  # Extract left half of the image
right_image = img[0:720, 1280:2560]  # Extract right half of the image

# Create a combined view of the original images
imgcat_source = cat2images(left_image, right_image)
HEIGHT = left_image.shape[0]
WIDTH = left_image.shape[1]

# Camera intrinsic parameters for left camera
camera_matrix0 = np.array([
    [2036.5, 1.3, 583.4],
    [0, 2028.6, 449.5],
    [0, 0, 1]])

# Distortion coefficients for left camera
distortion0 = np.array([[-0.3863, 0.5091, -0.0011, 0.001, -2.6353]])

# Camera intrinsic parameters for right camera
camera_matrix1 = np.array([
    [2036.5, 1.3, 583.4],
    [0, 2028.6, 449.5],
    [0, 0, 1]])

# Distortion coefficients for right camera
distortion1 = np.array([[-0.4256, 1.5578, -0.0023, 0.0005, -11.6757]])

# Rotation matrix between left and right cameras
R = np.array([
    [0.9999, 0.0012, 0.0164],
    [-0.0011, 1, -0.0019],
    [-0.0164, 0.0019, 0.9999]])

# Translation vector between left and right cameras
T = np.array([[-85.9802], [0.0723], [1.1451]])

# Compute rectification transforms for both cameras
(R_l, R_r, P_l, P_r, Q, validPixROI1, validPixROI2) = \
    cv2.stereoRectify(camera_matrix0, distortion0, camera_matrix1, distortion1, np.array([WIDTH, HEIGHT]), R,
                      T)  # Calculate rotation and projection matrices

# Apply rectification to both images
rect_left_image = undistort_and_remap(left_image, camera_matrix0, distortion0, R_l, P_l, (WIDTH, HEIGHT))
rect_right_image = undistort_and_remap(right_image, camera_matrix1, distortion1, R_r, P_r, (WIDTH, HEIGHT))

# Create and save the combined rectified image
imgcat_out = cat2images(rect_left_image, rect_right_image)
cv2.imwrite('imgcat_out.jpg', imgcat_out)
print(f"Done! Saved imgcat_out.jpg") 