import os

import cv2
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

import numpy as np
from PIL import Image, ImageTk
from SIFT_detector_1 import detect_sift_keypoints
from embed_watermark_2 import embed_watermark
from extract_watermark_3 import extract_watermark
from utils.helper import crop_image, rotate_image

# Global state
carrier_path = None
watermark_paths = []
watermark_bits = []
tampered_image_path = None
keypoints = None
image = None
embed_locs = []
min_spacing = 0
image_tk = None
wm_image_tks = []
embedded_image_tk = None
recovery_image_tk = None
tampered_image_tk = None
extracted_wm_tk = None

# GUI setup
root = tk.Tk()
root.title("Watermark Steganography GUI")
root.geometry("850x850")

# Make columns and rows expand evenly
for i in range(3):  # 3 columns
    root.grid_columnconfigure(i, weight=1, uniform="col")

for i in range(2):  # 2 rows
    root.grid_rowconfigure(i, weight=1, uniform="row")


# ==== Top Row: 3 Frames ====
main_frame = tk.LabelFrame(root, text="1. Carrier Image", width=280, height=300, padx=5, pady=5)
main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

wm_frame = tk.LabelFrame(root, text="2. Watermark Images", padx=5, pady=5)
wm_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

embed_frame = tk.LabelFrame(root, text="3. Embed Watermark", padx=5, pady=5)
embed_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")


# ==== Bottom Row: Combined Tampered Section ====
watermark_recovery_frame = tk.LabelFrame(root, text="4. Watermark Recovery", padx=5, pady=5)
watermark_recovery_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

check_frame = tk.LabelFrame(root, text="5. Tampering Detector", padx=5, pady=5)
check_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

auth_frame = tk.LabelFrame(root, text="6. Result Console", padx=5, pady=5)
auth_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

# ==== Main Frame Content ====
carrier_btn = tk.Button(main_frame, text="Load Carrier Image")
carrier_btn.pack()

main_image_label = tk.Label(main_frame)
main_image_label.pack()
carrier_kf_count_label = tk.Label(main_frame, text="")
carrier_kf_count_label.pack()

# ==== Watermark Frame Content ====
load_wm_btn = tk.Button(wm_frame, text="Load Watermark", state='disabled')
load_wm_btn.pack()

wm_image_labels = []
for i in range(3):
    label = tk.Label(wm_frame)
    label.pack(pady=5)
    wm_image_labels.append(label)

# ==== Embed Frame Content ====
embed_btn = tk.Button(embed_frame, text="Embed Watermark", state='disabled')
embed_btn.pack()

embedded_image_label = tk.Label(embed_frame)
embedded_image_label.pack()

embed_status_label = tk.Label(embed_frame, text="")
embed_status_label.pack(pady=5)

# ==== Watermark Recovery Frame Content ====
recover_btn = tk.Button(watermark_recovery_frame, text="Recover Watermark", state='disabled')
recover_btn.pack()

recovery_image_label = tk.Label(watermark_recovery_frame)
recovery_image_label.pack()

recovery_analysis_label = tk.Label(watermark_recovery_frame, text="")
recovery_analysis_label.pack()

recovery_analysis_label2 = tk.Label(watermark_recovery_frame, text="")
recovery_analysis_label2.pack()

# ==== Check Frame Content ====
load_tampered_btn = tk.Button(check_frame, text="Load Tampered Image", state='disabled')
load_tampered_btn.pack()

tampered_image_label = tk.Label(check_frame)
tampered_image_label.pack()

tampered_kf_count_label = tk.Label(check_frame, text="")
tampered_kf_count_label.pack()

# ==== Authenticity Frame Content ====

auth_result_label = tk.Label(auth_frame, text="Image Analysis", font=("Arial", 12, "bold"))
auth_result_label.pack(pady=5)

auth_top_row = tk.Frame(auth_frame)
auth_top_row.pack()

auth_analysis_label = tk.Label(auth_top_row, text="Image Authenticity:", font=("Arial", 10))
auth_analysis_label.pack(side="left", padx=(0, 10))

verifier_status_label = tk.Label(auth_top_row, text="N/A", font=("Arial", 10,), bg="gray", fg="white", pady=2)
verifier_status_label.pack(side="left")

authenticity_label = tk.Label(auth_frame, text="Authenticity Verifier: 0.0%", font=("Arial", 10))
authenticity_label.pack(pady=5)

separator = tk.Frame(auth_frame, height=1, bd=0, bg="gray", relief="flat")
separator.pack(fill="x", padx=10, pady=5)

auth_top_row_2 = tk.Frame(auth_frame)
auth_top_row_2.pack()

tampering_label = tk.Label(auth_top_row_2, text="Tampering Detector:", font=("Arial", 10))
tampering_label.pack(side="left", padx=(0, 10))

tampering_status_label = tk.Label(auth_top_row_2, text="N/A", font=("Arial", 10,), bg="gray", fg="white", pady=2)
tampering_status_label.pack(side="left")


match_count_label = tk.Label(auth_frame, text="Keypoints Matched: 0 / 0", font=("Arial", 10))
match_count_label.pack(pady=5)

separator = tk.Frame(auth_frame, height=1, bd=0, bg="gray", relief="flat")
separator.pack(fill="x", padx=10, pady=5)

rotate_btn = tk.Button(auth_frame, text="Rotate Image", state='disabled')
rotate_btn.pack(pady=5)

crop_btn = tk.Button(auth_frame, text="Crop Image", state='disabled')
crop_btn.pack(pady=5)

# ==== Function Definitions ====
def load_carrier():
    global carrier_path, keypoints, image, image_tk
    carrier_path = filedialog.askopenfilename(title="Select Carrier Image")
    if carrier_path:
        image, keypoints, _ = detect_sift_keypoints(carrier_path)
        img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)).resize((300, 300))
        image_tk = ImageTk.PhotoImage(img_pil)
        main_image_label.config(image=image_tk)
        carrier_kf_count_label.config(text=f"SIFT found {len(keypoints)} keypoints")
        load_wm_btn.config(state='normal')
        print("## Step 1: Load Carrier Image")
        print("Carrier image loaded: ", carrier_path)
        print(f"Keypoints detected: {len(keypoints)}\n")


def load_watermark():
    global watermark_paths, wm_image_tks
    if len(watermark_paths) >= 3:
        messagebox.showinfo("Limit Reached", "You can only load up to 3 watermark images.")
        return

    wm_path = filedialog.askopenfilename(title="Select Watermark Image")
    if wm_path:
        img = Image.open(wm_path)
        watermark_paths.append(wm_path)
        img_resized = img.resize((100, 100), resample=Image.NEAREST)
        tk_img = ImageTk.PhotoImage(img_resized)
        wm_image_tks.append(tk_img)

        # change to binary
        watermark = cv2.imread(wm_path, cv2.IMREAD_GRAYSCALE)
        wm_bits = (watermark > 128).astype(np.uint8).tolist()
        watermark_bits.append(wm_bits)

        wm_image_labels[len(watermark_paths)-1].config(image=tk_img)

        if len(watermark_paths) > 0:
            embed_btn.config(state='normal')
        print("## Step 2: Load up to 3 Watermark Images")
        print(f"Watermark image {len(watermark_paths)} loaded:", wm_path)
        print(f"Watermark bits loaded: {watermark_bits}")



def filter_keypoints_by_spacing(keypoints, min_distance):
    filtered = []
    seen = []
    for kp in keypoints:
        x, y = kp.pt
        if all(np.hypot(x - sx, y - sy) >= min_distance for sx, sy in seen):
            filtered.append(kp)
            seen.append((x, y))
    return filtered


def embed_watermark_gui():
    global image, embed_locs, embedded_image_tk, min_spacing, filtered_kpt
    if not carrier_path or len(watermark_paths) == 0:
        messagebox.showerror("Error", "Load carrier and at least one watermark image.")
        return

    print("\n## Step 3: Embed Watermarks to Carrier Image")
    try:
        embed_locs.clear()
        min_distance = simpledialog.askinteger("Spacing Filter", "Minimum spacing between keypoints (e.g., 20):", minvalue=1, initialvalue=100)
        if min_distance is None:
            return
        min_spacing = min_distance

        filtered_keypoints = filter_keypoints_by_spacing(keypoints, min_spacing)
        print(f"total_keypoints: {len(keypoints)} | filtered_keypoints: {len(filtered_keypoints)}")

        # pre-embed to handle noise
        for i in range(len(keypoints)):
            wm_path = watermark_paths[i % len(watermark_paths)]
            embedding_image, loc = embed_watermark(image, keypoints, wm_path, i)

        cv2.imwrite("watermarked_output.png", embedding_image)

        # filtered-embedding
        for i in range(len(filtered_keypoints)):
            wm_path = watermark_paths[i % len(watermark_paths)]
            embedding_image, loc = embed_watermark(image, filtered_keypoints, wm_path, i)
            embed_locs.append(loc)

        cv2.imwrite("watermarked_output.png", embedding_image)

        vis_image = embedding_image.copy()
        for loc in embed_locs:
            cv2.circle(vis_image, (loc[0], loc[1]), radius=6, color=(0, 255, 0), thickness=2)
        img_pil = Image.fromarray(cv2.cvtColor(vis_image, cv2.COLOR_BGR2RGB)).resize((300, 300))
        embedded_image_tk = ImageTk.PhotoImage(img_pil)
        embedded_image_label.config(image=embedded_image_tk)

        embed_status_label.config(text=f"Watermarks embedded at {len(embed_locs)} filtered keypoints")
        recover_btn.config(state='normal')
        print(f"embedded_location: {embed_locs}")

    except Exception as e:
        messagebox.showerror("Embedding Failed", str(e))

def extract_watermark_gui():
    global recovery_image_tk, extracted_wm_tk
    print("\n## Step 4: Watermark Recovery")
    # 4.1 Re-apply SIFT detection
    embedded_img, kp_embedded, desc_embedded = detect_sift_keypoints('watermarked_output.png')
    # filter keypoints spacing
    filtered_keypoints = filter_keypoints_by_spacing(kp_embedded, min_spacing)
    print(f"total_keypoints: {len(kp_embedded)} | filtered_keypoints: {len(filtered_keypoints)}")

    num_keypoints_to_use = len(filtered_keypoints)
    recovery_image_label.config(text=f"{min_spacing} SIFT found {len(kp_embedded)} keypoints.\nUse only {num_keypoints_to_use} keypoints")

    recovered_blocks = []
    for idx in range(len(filtered_keypoints)):
        block_bits = extract_watermark(
            embedded_img, kp_embedded, keypoint_index=idx
        )
        recovered_blocks.append(block_bits.tolist())

    vis_image = embedded_img.copy()
    counter = 0
    matched_kp_count = 0
    for kp in filtered_keypoints:
        x, y = int(kp.pt[0]), int(kp.pt[1])
        if recovered_blocks[counter] in watermark_bits:
            cv2.circle(vis_image, (x,y), radius=6, color=(0, 255, 0), thickness=2)
            matched_kp_count += 1
        else:
            cv2.circle(vis_image, (x,y), radius=6, color=(0, 0, 255), thickness=2)
        counter += 1

    img_pil = Image.fromarray(cv2.cvtColor(vis_image, cv2.COLOR_BGR2RGB)).resize((300, 300))
    recovery_image_tk = ImageTk.PhotoImage(img_pil)
    recovery_image_label.config(image=recovery_image_tk)
    load_tampered_btn.config(state='normal')
    recovery_analysis_label.config(text=f"Keypoints Matched: {matched_kp_count} / {len(embed_locs)}")
    recovery_analysis_label2.config(text=f"Authenticity Level: { (matched_kp_count / len(embed_locs) * 100):.2f}% ")

def load_test_image(target_image_path):
    global tampered_image_path, tampered_image_tk, extracted_wm_tk
    print("\n## Step 4: Load up Test Image")
    print("uploading test image...")

    # 4.1 Re-apply SIFT detection
    embedded_img, kp_embedded, desc_embedded = detect_sift_keypoints(target_image_path)
    # filter keypoints spacing
    filtered_keypoints = filter_keypoints_by_spacing(kp_embedded, min_spacing)
    print(f"total_keypoints: {len(kp_embedded)} | filtered_keypoints: {len(filtered_keypoints)}")

    num_keypoints_to_use = len(filtered_keypoints)
    tampered_kf_count_label.config(text=f"SIFT found {len(kp_embedded)} keypoints.\nUse only {num_keypoints_to_use} keypoints")

    recovered_blocks = []
    for idx in range(len(filtered_keypoints)):
        block_bits = extract_watermark(
            embedded_img, kp_embedded, keypoint_index=idx
        )
        recovered_blocks.append(block_bits.tolist())

    vis_image = embedded_img.copy()
    counter = 0
    matched_kp_count = 0
    for kp in filtered_keypoints:
        x, y = int(kp.pt[0]), int(kp.pt[1])
        # print(f"({x},{y}): {recovered_blocks[counter]}")
        # print(f"({x},{y})")
        if recovered_blocks[counter] in watermark_bits:
            cv2.circle(vis_image, (x,y), radius=6, color=(0, 255, 0), thickness=2)
            matched_kp_count += 1
        else:
            cv2.circle(vis_image, (x,y), radius=6, color=(0, 0, 255), thickness=2)
        counter += 1

    img_pil = Image.fromarray(cv2.cvtColor(vis_image, cv2.COLOR_BGR2RGB)).resize((300, 300))
    tampered_image_tk = ImageTk.PhotoImage(img_pil)
    tampered_image_label.config(image=tampered_image_tk)
    match_count_label.config(text=f"Keypoints Matched: {matched_kp_count} / {len(embed_locs)}")

    ## result analysis
    # Compute integrity percentage
    authenticity_percent = matched_kp_count / len(embed_locs) * 100 if filtered_keypoints else 0
    authenticity_label.config(text=f"Authenticity Level: {authenticity_percent:.2f}%")
    rotate_btn.config(state='normal')
    crop_btn.config(state='normal')

    # Set verification badge
    if authenticity_percent >= 80:
        verifier_status_label.config(text="Yes", bg="green")
    else:
        verifier_status_label.config(text="No", bg="red")

    if authenticity_percent >= 80:
        tampering_status_label.config(text="Yes", bg="green")
    else:
        tampering_status_label.config(text="No", bg="red")

def tamper_test():
    tampered_image_path = filedialog.askopenfilename(title="Select Test Image")
    if not tampered_image_path:
        return

    load_test_image(tampered_image_path)

def rotate():
    input_path = "watermarked_output.png"
    output_dir = os.path.dirname(input_path) or "."
    angle = 90
    img = cv2.imread(input_path)
    if img is None:
        print("Failed to load 'watermarked_output.png'")
        return

    # Rotate and save
    rotated = rotate_image(img, angle)
    rotated_path = os.path.join(output_dir, "watermarked_rotated_output.png")
    cv2.imwrite(rotated_path, rotated)
    # print(f"Rotated image saved to {rotated_path}")
    load_test_image("watermarked_rotated_output.png")

def crop():
    input_path = "watermarked_output.png"
    output_dir = os.path.dirname(input_path) or "."
    crop_percent = 0.2
    img = cv2.imread(input_path)
    if img is None:
        print("Failed to load 'watermarked_output.png'")
        return

    cropped = crop_image(img, crop_percent)
    cropped_path = os.path.join(output_dir, "watermarked_cropped_output.png")
    cv2.imwrite(cropped_path, cropped)
    # print(f"Cropped image saved to {cropped_path}")
    load_test_image("watermarked_cropped_output.png")

# ==== Button Callbacks ====
carrier_btn.config(command=load_carrier)
load_wm_btn.config(command=load_watermark)
embed_btn.config(command=embed_watermark_gui)
recover_btn.config(command=extract_watermark_gui)
load_tampered_btn.config(command=tamper_test)
rotate_btn.config(command=rotate)
crop_btn.config(command=crop)


# ==== Start GUI ====
root.mainloop()
