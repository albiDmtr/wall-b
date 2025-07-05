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

def crop_lower_middle(image):
    height, width, channels = image.shape

    top = height // 3
    bottom = height

    left = width // 6
    right = width - width // 6

    cropped = image[top:bottom, left:right]
    
    return cropped

def create_obstacle_map(disp_map, rgb=False):
    depth_map = disparity_to_m(disp_map)

    # compensate for camera height
    height, width = depth_map.shape
    y_indices = np.arange(height).reshape(-1, 1)
    scaling_factor = 1.4 - (1.4 - 0.6) * y_indices / (height - 1)
    
    # Apply scaling to compensate for camera height
    compensated_depth = depth_map * scaling_factor

    # create obstacle map based on depth thresholds
    cutoff_depth = 1.6 # pixels further than this are ignored
    min_depth = 1.2 # pixels closer than this will be 1
    obstacle_map = np.clip((cutoff_depth - compensated_depth) / (cutoff_depth - min_depth), 0, 1)
    
    if rgb:
        # Convert to 3-channel RGB format
        obstacle_map = (obstacle_map * 255).astype(np.uint8)
        obstacle_map = np.stack([obstacle_map, obstacle_map, obstacle_map], axis=-1)
    
    return obstacle_map

def create_obstacle_profile(depth_map, add_scale=True):
    obstacle_map = create_obstacle_map(depth_map, rgb=False)
    # Sum along each row and divide by width to get percentage (0-1)
    profile = np.sum(obstacle_map, axis=0) / obstacle_map.shape[0]
    return profile

def visualize_obstacle_profile(profile, add_scale=True):
    width = len(profile)
    height = int(0.75 * width)
    
    if add_scale:
        # Create figure
        plt.figure(figsize=(10, 6))
        
        # Create the profile plot
        x = np.arange(width)
        plt.plot(x, profile, 'b-', linewidth=2)
        plt.ylim(0, 1)
        plt.xlabel('Horizontal Position')
        plt.ylabel('Obstacle Density')
        plt.title('Obstacle Profile')
        plt.grid(True)
        
        plt.tight_layout()
        
        # Convert the figure to an image array
        fig = plt.gcf()
        fig.canvas.draw()
        image_array = np.asarray(fig.canvas.buffer_rgba())
        plt.close()
        
        # Convert RGBA to RGB
        return cv2.cvtColor(image_array, cv2.COLOR_RGBA2RGB)
    else:
        # Original visualization without scale
        visualization = np.ones((height, width, 3), dtype=np.uint8) * 255
        
        # For each position in the profile
        for x in range(width):
            line_height = int(height * profile[x])
            if line_height > 0:
                visualization[height - line_height:height, x] = [0, 0, 0]
        
        return visualization

def create_binary_profile(obstacle_profile):
    profile_threshold = 0.35

    binary_profile = np.select(
        [obstacle_profile > profile_threshold],
        [1],
        default=0
    )
    
    return binary_profile

def visualize_binary_profile(disp_map):
    binary_profile = create_binary_profile(disp_map)
    width = len(binary_profile)
    height = int(0.75 * width)
    
    # Create a white image (255, 255, 255)
    visualization = np.ones((height, width, 3), dtype=np.uint8) * 255
    # For each position in the profile
    for x in range(width):
        if binary_profile[x] == 1:
            # Fill the entire column with red (0, 0, 255) if there's an obstacle
            visualization[:, x] = [0, 0, 255]
    
    return visualization

def binary_profile_from_frame(frame, image_displayer=None):
    left, right = undistort_rectify(frame)
    cropped_left = crop_lower_middle(left)
    cropped_right = crop_lower_middle(right)
    disp_map = disparity_map(cropped_left, cropped_right)

    if image_displayer is not None:
        # normalize disp_map and create that heatmap-like visualization
        normalized_disp_map = cv2.normalize(disp_map, None, 0, 255, cv2.NORM_MINMAX)
        heatmap = cv2.applyColorMap(normalized_disp_map, cv2.COLORMAP_JET)
        image_displayer.update(heatmap)

    obstacle_profile = create_obstacle_profile(disp_map)
    binary_profile = create_binary_profile(obstacle_profile)

    return binary_profile

def is_moving(prev_frame, curr_frame, template_size=50):
    # Extract template from center of previous frame
    h, w = prev_frame.shape[:2]
    template = prev_frame[h//2-template_size//2:h//2+template_size//2,
                         w//2-template_size//2:w//2+template_size//2]
    
    # Search for template in current frame
    result = cv2.matchTemplate(curr_frame, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    
    # Check if template moved significantly
    center_x, center_y = w//2, h//2
    displacement = np.sqrt((max_loc[0] - center_x)**2 + (max_loc[1] - center_y)**2)
    
    print(displacement)

    return displacement > 20 # pixels