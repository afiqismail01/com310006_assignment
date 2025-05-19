import numpy as np

def extract_watermark(watermarked_img, keypoints, keypoint_index):
    kp = keypoints[keypoint_index]
    x, y = int(kp.pt[0]), int(kp.pt[1])

    # Ensure 3x3 patch fits within the image
    if y - 1 < 0 or y + 2 > watermarked_img.shape[0] or x - 1 < 0 or x + 2 > watermarked_img.shape[1]:
        print(f"Keypoint {keypoint_index} at ({x}, {y}) is too close to the edge.")
        return None

    patch = watermarked_img[y-1:y+2, x-1:x+2]
    extracted_bits = np.zeros((3, 3), dtype=np.uint8)

    for i in range(3):
        for j in range(3):
            extracted_bits[i, j] = patch[i, j, 0] & 1  # LSB from blue channel

    return extracted_bits
