import cv2
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

import numpy as np
from PIL import Image, ImageTk
from SIFT_detector_1 import detect_sift_keypoints
from embed_watermark_2 import embed_watermark
from extract_watermark_3 import extract_watermark_by_coords
from tampering_detector_4 import detect_tampering_by_coords

# Global state
carrier_path = None
watermark_paths = []
tampered_image_path = None
keypoints = None
image = None
embed_locs = []
image_tk = None
wm_image_tks = []
embedded_image_tk = None
tampered_image_tk = None
extracted_wm_tk = None

# GUI setup
root = tk.Tk()
root.title("Watermark Steganography GUI")
root.geometry("1600x850")

# ==== Top Row: 3 Frames ====
main_frame = tk.LabelFrame(root, text="Main Image", padx=5, pady=5)
main_frame.grid(row=0, column=0, padx=10, pady=10)

wm_frame = tk.LabelFrame(root, text="Watermark Images", padx=5, pady=5)
wm_frame.grid(row=0, column=1, padx=10, pady=10)

embed_frame = tk.LabelFrame(root, text="Embed Watermark", padx=5, pady=5)
embed_frame.grid(row=0, column=2, padx=10, pady=10)

# ==== Bottom Row: Combined Tampered Section ====
check_frame = tk.LabelFrame(root, text="Check Tampered Image & Extracted Watermark", padx=5, pady=5)
check_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# ==== Main Frame Content ====
carrier_btn = tk.Button(main_frame, text="Load Carrier Image")
carrier_btn.pack()

main_image_label = tk.Label(main_frame)
main_image_label.pack()

# ==== Watermark Frame Content ====
load_wm_btn = tk.Button(wm_frame, text="Load Watermark", state='disabled')
load_wm_btn.pack()

wm_image_labels = []
for i in range(3):
    label = tk.Label(wm_frame)
    label.pack(pady=5)
    wm_image_labels.append(label)

# ==== Embed Frame Content ====
embed_btn = tk.Button(embed_frame, text="Embed", state='disabled')
embed_btn.pack(pady=5)

embedded_image_label = tk.Label(embed_frame)
embedded_image_label.pack()

embed_status_label = tk.Label(embed_frame, text="")
embed_status_label.pack(pady=5)

# ==== Check Frame Content ====
load_tampered_btn = tk.Button(check_frame, text="Load Tampered Image")
load_tampered_btn.pack(pady=5)

tampered_image_label = tk.Label(check_frame)
tampered_image_label.pack(side=tk.LEFT, padx=20)

extracted_wm_label = tk.Label(check_frame)
extracted_wm_label.pack(side=tk.LEFT, padx=20)

check_status_label = tk.Label(check_frame, text="")
check_status_label.pack(side=tk.LEFT, padx=20)

# ==== Function Definitions ====
def load_carrier():
    global carrier_path, keypoints, image, image_tk
    carrier_path = filedialog.askopenfilename(title="Select Carrier Image")
    if carrier_path:
        image, keypoints, _ = detect_sift_keypoints(carrier_path)
        img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)).resize((300, 300))
        image_tk = ImageTk.PhotoImage(img_pil)
        main_image_label.config(image=image_tk)
        load_wm_btn.config(state='normal')
        print("Carrier image loaded:", carrier_path)


def load_watermark():
    global watermark_paths, wm_image_tks
    if len(watermark_paths) >= 3:
        messagebox.showinfo("Limit Reached", "You can only load up to 3 watermark images.")
        return

    path = filedialog.askopenfilename(title="Select Watermark Image")
    if path:
        watermark_paths.append(path)
        img = Image.open(path)
        img_resized = img.resize((100, 100), resample=Image.NEAREST)
        tk_img = ImageTk.PhotoImage(img_resized)
        wm_image_tks.append(tk_img)
        wm_image_labels[len(watermark_paths)-1].config(image=tk_img)

        if len(watermark_paths) > 0:
            embed_btn.config(state='normal')
        print(f"Watermark image {len(watermark_paths)} loaded:", path)


def embed_watermark_gui():
    global image, embed_locs, embedded_image_tk
    if not carrier_path or len(watermark_paths) == 0:
        messagebox.showerror("Error", "Load carrier and at least one watermark image.")
        return

    try:
        embed_locs.clear()
        num_keypoints_to_use = len(keypoints)

        for i in range(min(num_keypoints_to_use, len(keypoints))):
            wm_path = watermark_paths[i % len(watermark_paths)]
            image, loc = embed_watermark(image, keypoints, wm_path, i)
            embed_locs.append(loc)

        cv2.imwrite("watermarked_output.png", image)

        vis_image = image.copy()
        for loc in embed_locs:
            cv2.circle(vis_image, (loc[0], loc[1]), radius=6, color=(0, 255, 0), thickness=2)
        img_pil = Image.fromarray(cv2.cvtColor(vis_image, cv2.COLOR_BGR2RGB)).resize((300, 300))
        embedded_image_tk = ImageTk.PhotoImage(img_pil)
        embedded_image_label.config(image=embedded_image_tk)

        embed_status_label.config(text=f"Different watermarks embedded at {len(embed_locs)} keypoints")

    except Exception as e:
        messagebox.showerror("Embedding Failed", str(e))


def load_tampered_image():
    global tampered_image_path, tampered_image_tk, extracted_wm_tk
    tampered_image_path = filedialog.askopenfilename(title="Select Tampered Image")
    if not tampered_image_path:
        return

    tampered_img_cv = cv2.imread(tampered_image_path)
    vis_img = tampered_img_cv.copy()

    if embed_locs and watermark_paths:
        ref_wm = cv2.imread(watermark_paths[0], cv2.IMREAD_GRAYSCALE)
        tampered_points = detect_tampering_by_coords(tampered_img_cv, embed_locs, ref_wm)

        for i, (x, y) in enumerate(embed_locs):
            x, y = int(x), int(y)
            if 0 <= x < vis_img.shape[1] and 0 <= y < vis_img.shape[0]:
                color = (0, 255, 0) if (i not in tampered_points) else (0, 0, 255)
                cv2.circle(vis_img, (x, y), radius=6, color=color, thickness=2)

        img_pil = Image.fromarray(cv2.cvtColor(vis_img, cv2.COLOR_BGR2RGB)).resize((300, 300))
        tampered_image_tk = ImageTk.PhotoImage(img_pil)
        tampered_image_label.config(image=tampered_image_tk)

        if not tampered_points:
            check_status_label.config(text="✅ All watermarks intact.")
        else:
            check_status_label.config(text=f"⚠️ Tampering at {len(tampered_points)} of {len(embed_locs)} locations.")

        print("Tampered locations (indexes):", tampered_points)


# ==== Button Callbacks ====
carrier_btn.config(command=load_carrier)
load_wm_btn.config(command=load_watermark)
embed_btn.config(command=embed_watermark_gui)
load_tampered_btn.config(command=load_tampered_image)

# ==== Start GUI ====
root.mainloop()
