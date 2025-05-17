import numpy as np
from extract_watermark_3 import extract_watermark_by_coords

def is_watermark_intact_by_coords(img, x, y, reference_watermark):
    try:
        extracted = extract_watermark_by_coords(img, x, y)
        extracted_bits = (extracted > 128).astype(np.uint8)
        ref_bits = (reference_watermark > 128).astype(np.uint8)
        return np.array_equal(extracted_bits, ref_bits)
    except:
        return False

def detect_tampering_by_coords(image, embed_locs, reference_wm, threshold=0.9):
    tampered_indices = []

    ref_bin = (reference_wm > 0).astype(np.uint8)

    for idx, (x, y) in enumerate(embed_locs):
        extracted = extract_watermark_by_coords(image, x, y)
        if extracted is None:
            tampered_indices.append(idx)
            continue

        extracted_bin = (extracted > 0).astype(np.uint8)

        # Calculate similarity
        similarity = np.mean(ref_bin == extracted_bin)
        if similarity < threshold:
            tampered_indices.append(idx)

    return tampered_indices

