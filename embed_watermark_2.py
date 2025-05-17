import cv2
import numpy as np

def embed_watermark(img, keypoints, watermark_path, keypoint_index=0):
    watermark = cv2.imread(watermark_path, cv2.IMREAD_GRAYSCALE)
    wm_bits = (watermark > 128).astype(np.uint8)
    print("Watermark bits being embedded:")
    print(wm_bits)

    kp = keypoints[keypoint_index]
    x, y = int(kp.pt[0]), int(kp.pt[1])

    if y - 1 < 0 or y + 2 > img.shape[0] or x - 1 < 0 or x + 2 > img.shape[1]:
        raise ValueError("Keypoint too close to image edge for 3x3 embedding.")

    region = img[y-1:y+2, x-1:x+2].copy()

    for i in range(3):
        for j in range(3):
            blue_val = region[i, j, 0]
            blue_val = (blue_val & 0xFE) | wm_bits[i, j]
            region[i, j, 0] = blue_val

    img[y-1:y+2, x-1:x+2] = region

    return img, (x, y)

