import numpy as np
import cv2

# Step 2.1: Create a 3x3 binary watermark
watermark = np.array([
    [255,   0, 255],
    [  0, 255,   0],
    [255,   0, 255]
], dtype=np.uint8)

# Save it (optional) just to see it
cv2.imwrite('watermark.png', watermark)
