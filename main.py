import cv2
from SIFT_detector_1 import detect_sift_keypoints
from embed_watermark_2 import embed_watermark

carrier_image_path = 'carrier_image.png'
watermark_path = 'watermark.png'
output_path = 'watermarked_image.png'


# handle image upload and detect keypoints
img, keypoints, descriptors = detect_sift_keypoints(carrier_image_path)
print(f"keypoints: {len(keypoints)}")

# Embed at first 3 keypoints, collect (x, y) locations
embed_locs = []
for i in range(3):
    img, loc = embed_watermark(img, keypoints, watermark_path, keypoint_index=i)
    embed_locs.append(loc)

cv2.imwrite(output_path, img)
