import cv2
from cam.hitnet import HitNet, ModelType, draw_disparity
import os
import time
import numpy as np
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SCRIPT_DIR = Path(__file__).parent.absolute()
frame_width = 1280
frame_height = 720

def load_calibration_params(json_path=None):
    if json_path is None:
        json_path = SCRIPT_DIR / 'calibrate' / 'camera_calibration.json'
    else:
        json_path = Path(json_path).absolute()
    
    with open(json_path, 'r') as f:
        params = json.load(f)
    
    return {
        'left_camera_matrix': np.array(params['left_camera_matrix']),
        'left_distortion': np.array(params['left_distortion']),
        'right_camera_matrix': np.array(params['right_camera_matrix']),
        'right_distortion': np.array(params['right_distortion']),
        'R': np.array(params['R']),
        'T': np.array(params['T'])
    }

def save_to_desktop(frame):
    file_path = str(Path.home() / "Desktop")
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"capture_{timestamp}.jpg"
    filepath = os.path.join(file_path, filename)
    cv2.imwrite(filepath, frame)

camera_params = None
def undistort_rectify(frame):
    global camera_params
    if camera_params is None:
        camera_params = load_calibration_params()
    
    # split the stereo image
    left_image = frame[:, :frame_width]
    right_image = frame[:, frame_width:]
    
    (R_l, R_r, P_l, P_r, Q, validPixROI1, validPixROI2) = cv2.stereoRectify(
        camera_params['left_camera_matrix'],
        camera_params['left_distortion'],
        camera_params['right_camera_matrix'],
        camera_params['right_distortion'],
        np.array([frame_width, frame_height]),
        camera_params['R'],
        camera_params['T']
    )
    
    # create rectification maps
    left_map_1, left_map_2 = cv2.initUndistortRectifyMap(
        camera_params['left_camera_matrix'],
        camera_params['left_distortion'],
        R_l,
        P_l,
        (frame_width, frame_height),
        cv2.CV_16SC2
    )
    right_map_1, right_map_2 = cv2.initUndistortRectifyMap(
        camera_params['right_camera_matrix'],
        camera_params['right_distortion'],
        R_r,
        P_r,
        (frame_width, frame_height),
        cv2.CV_16SC2
    )
    
    # apply rectification
    left_undistorted = cv2.remap(left_image, left_map_1, left_map_2, cv2.INTER_LINEAR)
    right_undistorted = cv2.remap(right_image, right_map_1, right_map_2, cv2.INTER_LINEAR)

    return left_undistorted, right_undistorted

def init_hitnet(model_size="240x320"):
    if model_size=="480x640":
        model_path = SCRIPT_DIR / 'hitnet' / 'models' / 'eth3d' / 'saved_model_480x640' / 'model_float32.tflite'
    elif model_size=="240x320":
        model_path = SCRIPT_DIR / 'hitnet' / 'models' / 'eth3d' / 'saved_model_240x320' / 'model_float32.tflite'
    elif model_size=="120x160":
        model_path = SCRIPT_DIR / 'hitnet' / 'models' / 'eth3d' / 'saved_model_120x160' / 'model_float32.tflite'
    model_path = Path(model_path).as_posix()

    # initialize model
    hitnet_depth = HitNet(model_path, ModelType.eth3d)
    return hitnet_depth

hitnet_depth = None
def disparity_map(left_img, right_img):
    global hitnet_depth
    if hitnet_depth is None:
        hitnet_depth = init_hitnet()

    # estimate the depth
    disparity_map = hitnet_depth(left_img, right_img)

    return disparity_map

def visualize_disparity(left_img, right_img):
    disp = disparity_map(left_img, right_img)

    # create depthmap
    depthmap = draw_disparity(disp)

    # creating disparity map visualization
    plt.figure(figsize=(12, 8))
    im = plt.imshow(disp, cmap='viridis')
    plt.colorbar(im, label='Disparity Value')
    plt.title('Disparity Map Visualization')
    plt.xlabel('Image Width')
    plt.ylabel('Image Height')
    
    fig = plt.gcf()
    fig.canvas.draw()
    image_array = np.asarray(fig.canvas.buffer_rgba())
    # Convert RGBA to RGB
    image_array = cv2.cvtColor(image_array, cv2.COLOR_RGBA2RGB)

    plt.close()

    # resize images to match height of left_img
    target_h, target_w = left_img.shape[:2]
    
    depthmap = cv2.resize(depthmap, (target_w, target_h))
    image_array = cv2.resize(image_array, (target_w, target_h))
    
    combined_image = np.hstack((left_img, depthmap, image_array))
    
    return combined_image

def load_hitnet_params(json_path=None):
    if json_path is None:
        json_path = SCRIPT_DIR / 'hitnet' / 'hitnet_to_m.json'
    else:
        json_path = Path(json_path).absolute()
    
    with open(json_path, 'r') as f:
        params = json.load(f)
    
    return params['fB'], params['d_null']

# Convert disparity to distance from camera in meters
fB, d_null = None, None
def disparity_to_m(disparity_val):
    global fB, d_null

    if fB is None or d_null is None:
        fB, d_null = load_hitnet_params()

    return fB / (disparity_val - d_null)