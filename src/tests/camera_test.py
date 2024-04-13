import cv2
import time

# Loop through potential device indices
for index in range(0, 10):  # Adjust range if you have more devices
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print(f"Cannot open camera at index {index}")
    else:
        print(f"Trying camera at index {index}")
        ret, frame = cap.read()
        if not ret:
            print(f"Can't receive frame from index {index}")
        else:
            cv2.imshow('Webcam Live', frame)
            cv2.waitKey(5000)  # Shows the frame for 5000 ms (5 seconds)
            cv2.destroyAllWindows()

        cap.release()
        time.sleep(1)  # Wait a bit before trying the next index