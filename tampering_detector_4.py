def tampering_detector(recovered_blocks, wm_bits, keypoint_index):
    if hasattr(wm_bits, 'tolist'):  # Convert to list if still NumPy array
        wm_bits = wm_bits.tolist()

    if keypoint_index >= len(recovered_blocks):
        raise IndexError("Keypoint index out of range of recovered blocks.")

    return recovered_blocks[keypoint_index] == wm_bits
