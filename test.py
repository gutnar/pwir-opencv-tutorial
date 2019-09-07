# 1. Capture frames from camera
# 2. Threshold colors for ball
# 3. Maybe try to remove noise
# 4. Use blob detection to locate balls
# 5. Draw a circle around your ball

import cv2
import numpy as np
import sys
from functools import partial

ranges = [
    [0, 0, 0],
    [179, 255, 255]
]

if len(sys.argv) < 2:
    exit("Enter color name")

color_name = sys.argv[1]

with open("colors.csv", "r") as file:
    for line in file:
        data = line.split(",")

        if data[0] == color_name:
            ranges[0] = [int(i) for i in data[1:4]]
            ranges[1] = [int(i) for i in data[4:]]

def update_range(i, j, value):
    ranges[i][j] = value

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
    mask = cv2.inRange(hsv, tuple(ranges[0]), tuple(ranges[1]))
    cv2.imshow("mask", mask)

    # Remove noise
    kernel = np.ones((5, 5), np.uint8)
    eroded = cv2.erode(mask, kernel)
    dilated = cv2.dilate(mask, kernel)
    cv2.imshow("less noise", dilated)

    # Keyboard input
    key = cv2.waitKey(10)

    if key & 0xFF == ord("s"):
        with open("colors.csv", "a") as file:
            file.write(color_name + ",")
            file.write(",".join([str(i) for i in sum(ranges, [])]))
            file.write("\n")

    if key & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
