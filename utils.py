import cv2
import numpy as np


def apply_color_mask(src, color_range):
    # Convert to HSV and apply color mask
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, tuple(color_range[0]), tuple(color_range[1]))

    # Remove noise (Google opencv morphological transformations)
    kernel = np.ones((3, 3), np.uint8)
    less_noise = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    return less_noise
