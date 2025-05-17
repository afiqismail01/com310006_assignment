import cv2
from SIFT_detector_1 import detect_sift_keypoints
from embed_watermark_2 import embed_watermark
from tampering_detector_4 import detect_tampering_by_coords

carrier_image_path = 'carrier_image.png'
watermark_path = 'watermark.png'
output_path = 'watermarked_output.png'


# Detect keypoints using SIFT
img, keypoints, descriptors = detect_sift_keypoints(carrier_image_path)
print(f"keypoints: {len(keypoints)}")

# Embed at first 3 keypoints, collect (x, y) locations
embed_locs = []
for i in range(3):
    img, loc = embed_watermark(img, keypoints, watermark_path, keypoint_index=i)
    embed_locs.append(loc)

cv2.imwrite(output_path, img)

# Detect any tampering activities to the watermarked_image
verified_img = cv2.imread("watermarked_image_2.png")
ref_wm = cv2.imread(watermark_path, cv2.IMREAD_GRAYSCALE)

tampered = detect_tampering_by_coords(verified_img, embed_locs, ref_wm)

if not tampered:
    print("✅ No tampering detected.")
else:
    print("⚠️ Tampering detected at coordinates:", tampered)