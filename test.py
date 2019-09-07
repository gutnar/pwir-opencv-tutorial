# 1. Capture frames from camera
# 2. Threshold colors for ball
# 3. Maybe try to remove noise
# 4. Use blob detection to locate balls
# 5. Draw a circle around your ball

import cv2
import numpy as np
from functools import partial

import config


color_name = input("Color name: ")

try:
    color_range = config.get_color_range(color_name)
except KeyError:
    color_range = [
        [0, 0, 0],
        [179, 255, 255]
    ]


def update_range(i, j, value):
    color_range[i][j] = value

cv2.namedWindow("frame")
cv2.createTrackbar("h_min", "frame", 0, 179, partial(update_range, 0, 0))
cv2.createTrackbar("h_max", "frame", 179, 179, partial(update_range, 1, 0))
cv2.createTrackbar("s_min", "frame", 0, 255, partial(update_range, 0, 1))
cv2.createTrackbar("s_max", "frame", 255, 255, partial(update_range, 1, 1))
cv2.createTrackbar("v_min", "frame", 0, 255, partial(update_range, 0, 2))
cv2.createTrackbar("v_max", "frame", 255, 255, partial(update_range, 1, 2))

cap = cv2.VideoCapture(0)

while cap.isOpened():
    _, frame = cap.read()
    cv2.imshow("frame", frame)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, tuple(color_range[0]), tuple(color_range[1]))
    cv2.imshow("mask", mask)

    # Remove noise
    kernel = np.ones((5, 5), np.uint8)
    eroded = cv2.erode(mask, kernel)
    dilated = cv2.dilate(mask, kernel)
    cv2.imshow("less noise", dilated)

    # Keyboard input
    key = cv2.waitKey(10)

    if key & 0xFF == ord("s"):
        config.set_color_range(color_name, color_range[0], color_range[1])

    if key & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
