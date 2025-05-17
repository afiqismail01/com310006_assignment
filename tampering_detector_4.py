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

def detect_tampering_by_coords(img, embed_locations, reference_watermark):
    tampered_coords = []
    for (x, y) in embed_locations:
        if not is_watermark_intact_by_coords(img, x, y, reference_watermark):
            tampered_coords.append((x, y))
    return tampered_coords
