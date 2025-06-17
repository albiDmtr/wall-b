import random
import math
from cam.stereo_processing import binary_profile_from_frame, visualize_binary_profile, is_moving
from cam.stereo_cam import stereo_cam
from move.motor_driver import move_s, turn_s, move, turn, stop
from object_detection.efficientdet import EfficientDet
from cam.show_image import ImageDisplayer

class guidance:
    def __init__(self):
        self._cam = stereo_cam()
        self._cam.start()
        self._detector = EfficientDet()
        self._img_window = None
    
    def _has_obstacle(self, profile):
        min_continuous_obstacle_width = 4
        has_obstacle_ahead = False

        for i in range(len(profile) - min_continuous_obstacle_width + 1):
            if sum(profile[i:i + min_continuous_obstacle_width]) == min_continuous_obstacle_width:
                has_obstacle_ahead = True
        
        return has_obstacle_ahead
    
    def _cut_edge_off_profile(self, profile):
        eitht_of_len = len(profile) // 8
        seven_eighth_of_len = (len(profile) * 7) // 8
        binary_profile_cut = profile[eitht_of_len:seven_eighth_of_len]

        return binary_profile_cut
    
    def _turn_until_clear(self, turn_direction):
        turn_duration = random.uniform(3, 5)
        while True:
            turn_s(turn_duration, turn_direction)
            frame = self._cam.capture()
            binary_profile = binary_profile_from_frame(frame)
            binary_profile_cut = self._cut_edge_off_profile(binary_profile)

            if not self._has_obstacle(binary_profile_cut):
                break

    def move_randomly(self, visualize=False):
        # Randomly move the robot in the area while avoiding obstacles

        # turn in a random direction initially
        turn_direction = random.choice(["left", "right"])
        turn_duration = random.uniform(0, 3)
        turn_s(turn_duration, turn_direction)

        prev_frame = None
        while True:
            print("Entering loop")
            move("forward")

            frame = self._cam.capture()

            # check if the robot is stuck
            if prev_frame is not None and not is_moving(prev_frame, frame):
                print("Help stepbro, I'm stuck")
                #stop()
                #break

            prev_frame = frame

            # check if there are obstacles in the way
            binary_profile = binary_profile_from_frame(frame)

            if visualize:
                if self._img_window is None:
                    self._img_window = ImageDisplayer()
                binary_profile_vis = visualize_binary_profile(binary_profile)

            # cut side first and last 1/8 off of the binary profile
            binary_profile_cut = self._cut_edge_off_profile(binary_profile)

        
            if self._has_obstacle(binary_profile_cut):
                stop()

                # check if the obstacle is on the left or right
                half_len = len(binary_profile_cut) // 2
                left_profile = binary_profile_cut[:half_len]
                right_profile = binary_profile_cut[half_len:]

                if self._has_obstacle(left_profile):
                    print("Obstacle on left")
                    self._turn_until_clear("right")
                elif self._has_obstacle(right_profile):
                    print("Obstacle on right")
                    self._turn_until_clear("left")
                else:
                    print("Obstacle in front")
                    # turn in a random direction between 2-4 seconds
                    turn_direction = random.choice(["left", "right"])
                    self._turn_until_clear(turn_direction)

                if self._img_window is not None:
                    self._img_window.update(binary_profile_vis[:, ::-1])
            

            

