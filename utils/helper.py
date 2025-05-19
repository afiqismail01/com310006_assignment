import cv2
import os

def rotate_image(image, angle):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    return rotated

def crop_image(image, crop_percent):
    h, w = image.shape[:2]
    ch = int(h * crop_percent / 2)
    cw = int(w * crop_percent / 2)
    return image[ch:h - ch, cw:w - cw]