import cv2
import numpy as np

from SIFT_detector_1 import detect_sift_keypoints
from embed_watermark_2 import embed_watermark
from extract_watermark_3 import extract_watermark
from tampering_detector_4 import tampering_detector

carrier_image_path = 'carrier_image.png'
watermark_path = 'watermark_1.png'
watermarked_path = 'watermarked_output.png'
tampered_path = 'watermarked_output_2.png'
keypoint_range = 1100

# Step 1: Detect keypoints in original image
original_img, kp_original, desc_original = detect_sift_keypoints(carrier_image_path)

# Step 2: Load and binarize watermark
watermark = cv2.imread(watermark_path, cv2.IMREAD_GRAYSCALE)
wm_bits = (watermark > 128).astype(np.uint8)
# print(wm_bits)

# Step 3: Embed watermarks to the defined keypoints
for i in range(keypoint_range):
    img, _ = embed_watermark(original_img, kp_original, watermark_path, keypoint_index=i)
cv2.imwrite(watermarked_path, img)

# Step 4: Reapply SIFT to detect keypoints on the embedded carrier image
embedded_img, kp_embedded, desc_embedded = detect_sift_keypoints(watermarked_path)

print(f"carrier_keypoints: {len(kp_original)} | embedded_keypoints: {len(kp_embedded)}")
print(f"watermark: {wm_bits.tolist()}")

# Step 5: Extract each block using descriptor matching
recovered_blocks = []

for idx in range(keypoint_range):
    block_bits = extract_watermark(
        embedded_img, kp_embedded, keypoint_index=idx
    )
    recovered_blocks.append(block_bits.tolist())

print(f"extracted_watermarks: {recovered_blocks}")
if len(recovered_blocks) != keypoint_range:
    print("tested image authentication: not authenticate / modified")
else:
    print(f"tested image authentication: original")

# Step 6: Detect any tampering attempts

matched_count = 0
for idx in range(keypoint_range):
    # print(f"RE: {recovered_blocks[idx]}")
    if recovered_blocks[idx] == wm_bits.tolist():
        matched_count += 1

print(f"matched_kp: {matched_count} / {keypoint_range}")
print(f"target image consistency: { matched_count / keypoint_range * 100}")


# matching_embedding_bits = tampering_detector(recovered_blocks, wm_bits.tolist())
# print(f"{matching_embedding_bits} / {len(recovered_blocks)} blocks match the embedded watermark.")

# if not tampered_blocks:
#     print("✅ No tampering detected.")
# else:
#     print("⚠️ Tampering detected in watermark blocks:", tampered_blocks)


