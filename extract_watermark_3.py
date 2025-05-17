import cv2
import numpy as np

def extract_watermark_by_coords(img, x, y):
    if y - 1 < 0 or y + 2 > img.shape[0] or x - 1 < 0 or x + 2 > img.shape[1]:
        raise ValueError("Coordinates too close to edge.")


    region = img[y-1:y+2, x-1:x+2]
    extracted_bits = np.zeros((3, 3), dtype=np.uint8)

    for i in range(3):
        for j in range(3):
            blue_val = region[i, j, 0]
            extracted_bits[i, j] = blue_val & 1

    return extracted_bits * 255

