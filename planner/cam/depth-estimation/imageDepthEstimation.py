import cv2
from hitnet import HitNet, ModelType, draw_disparity, draw_depth, CameraConfig, load_img
import numpy as np
from imread_from_url import imread_from_url
from pathlib import Path
import time

# TODO: The app crashes when running on the gpu
import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"  

if __name__ == '__main__':
		
	# Select model type
	# model_type = ModelType.middlebury
	# model_type = ModelType.flyingthings
	model_type = ModelType.eth3d

	if model_type == ModelType.middlebury:
		model_path = "models/middlebury_d400/saved_model_480x640/model_float32.tflite"
	elif model_type == ModelType.flyingthings:
		model_path = "models/flyingthings_finalpass_xl/saved_model_480x640/model_float32.tflite"
	elif model_type == ModelType.eth3d:
		model_path = "models/eth3d/saved_model_480x640/model_float32.tflite"

	# Initialize model
	hitnet_depth = HitNet(model_path, model_type)

	# Capture images
	frame_width = 1280
	frame_height = 720
	cap = cv2.VideoCapture(0)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2*frame_width)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

	ret, frame = cap.read()
	cap.release()

	left_img = frame[:, :frame_width]
	right_img = frame[:, frame_width:]

	# Estimate the depth
	disparity_map = hitnet_depth(left_img, right_img)

	color_disparity = draw_disparity(disparity_map)
	color_disparity = cv2.resize(color_disparity, (left_img.shape[1],left_img.shape[0]))

	cobined_image = np.hstack((left_img, right_img, color_disparity))

	desktop_path = str(Path.home() / "Desktop")
	timestamp = time.strftime("%Y%m%d_%H%M%S")
	filename = f"capture_{timestamp}.jpg"
	filepath = os.path.join(desktop_path, filename)
	cv2.imwrite(filepath, cobined_image)
