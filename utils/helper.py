import cv2
import os

import numpy as np

## help to return n-pixels space between keypoints
def filter_keypoints_by_spacing(keypoints, min_distance):
    filtered = []
    seen = []
    for kp in keypoints:
        x, y = kp.pt
        if all(np.hypot(x - sx, y - sy) >= min_distance for sx, sy in seen):
            filtered.append(kp)
            seen.append((x, y))
    return filtered

## generate a rotated image
def rotate_image(image, angle):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    return rotated

## generate a cropped image
def crop_image(image, crop_percent):
    h, w = image.shape[:2]
    ch = int(h * crop_percent / 2)
    cw = int(w * crop_percent / 2)
    return image[ch:h - ch, cw:w - cw]