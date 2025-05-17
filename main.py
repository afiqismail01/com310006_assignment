import cv2
from SIFT_detector_1 import detect_sift_keypoints

carrier_image_path = 'carrier_image.png'
img, keypoints, descriptors = detect_sift_keypoints(carrier_image_path)
print(f"keypoints: {len(keypoints)}")


