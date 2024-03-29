import cv2
import numpy as np


def get_color_range_mean(color_range):
    return tuple([
        (color_range[0][i] + color_range[1][i]) // 2
        for i in range(2)
    ])


def apply_color_mask(src, color_range):
    # Convert to HSV and apply color mask
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, tuple(color_range[0]), tuple(color_range[1]))

    # Remove noise (Google opencv morphological transformations)
    kernel = np.ones((3, 3), np.uint8)
    less_noise = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    return less_noise


def find_biggest_circle(src):
    contours, _hierarchy = cv2.findContours(src, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    circles = map(cv2.minEnclosingCircle, contours)
    circles = sorted(circles, key = lambda circle: circle[1])

    if len(circles):
        (x, y), radius = circles[-1]
        return (int(x), int(y)), int(radius)
