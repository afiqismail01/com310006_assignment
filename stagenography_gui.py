import cv2
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk
from SIFT_detector_1 import detect_sift_keypoints
from embed_watermark_2 import embed_watermark
from extract_watermark_3 import extract_watermark_by_coords
from tampering_detector_4 import detect_tampering_by_coords

# Global state
carrier_path = None
watermark_path = None
keypoints = None
image = None
embed_locs = []
image_tk = None
wm_image_tk = None
embedded_image_tk = None

# GUI setup
root = tk.Tk()
root.title("Watermark Steganography GUI")
root.geometry("1000x500")  # Adjusted width

# ==== Main Image Section ====
main_frame = tk.LabelFrame(root, text="Main Image", padx=5, pady=5)
main_frame.grid(row=0, column=0, padx=10, pady=10)

carrier_btn = tk.Button(main_frame, text="Load Carrier Image")
carrier_btn.pack()

main_image_label = tk.Label(main_frame)
main_image_label.pack()

# ==== Watermark Section ====
wm_frame = tk.LabelFrame(root, text="Watermark Image", padx=5, pady=5)
wm_frame.grid(row=0, column=1, padx=10, pady=10)

load_wm_btn = tk.Button(wm_frame, text="Load Watermark", state='disabled')
load_wm_btn.pack()

wm_image_label = tk.Label(wm_frame)
wm_image_label.pack()

# ==== Embed/Detect Section ====
embed_frame = tk.LabelFrame(root, text="Embed Watermark", padx=5, pady=5)
embed_frame.grid(row=0, column=2, padx=10, pady=10)

embed_btn = tk.Button(embed_frame, text="Embed", state='disabled')
embed_btn.pack(pady=5)

embedded_image_label = tk.Label(embed_frame)
embedded_image_label.pack()

embed_status_label = tk.Label(embed_frame, text="")
embed_status_label.pack(pady=5)

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
    global watermark_path, wm_image_tk
    path = filedialog.askopenfilename(title="Select Watermark Image")
    if path:
        watermark_path = path
        img = Image.open(path).resize((100, 100))
        wm_image_tk = ImageTk.PhotoImage(img)
        wm_image_label.config(image=wm_image_tk)
        embed_btn.config(state='normal')
        print("Watermark image loaded:", path)


def embed_watermark_gui():
    global image, embed_locs, image_tk, embedded_image_tk
    if not carrier_path or not watermark_path:
        messagebox.showerror("Error", "Load both carrier and watermark images first.")
        return

    index = simpledialog.askinteger("Keypoint Index", "Enter keypoint index (0-9):", minvalue=0, maxvalue=9)
    if index is None:
        return

    try:
        image, loc = embed_watermark(image, keypoints, watermark_path, index)
        embed_locs.clear()
        embed_locs.append(loc)
        cv2.imwrite("watermarked_output.png", image)

        img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)).resize((300, 300))
        embedded_image_tk = ImageTk.PhotoImage(img_pil)
        embedded_image_label.config(image=embedded_image_tk)
        embed_status_label.config(text="Watermark added")

    except Exception as e:
        messagebox.showerror("Embedding Failed", str(e))


# ==== Button Callbacks ====
carrier_btn.config(command=load_carrier)
load_wm_btn.config(command=load_watermark)
embed_btn.config(command=embed_watermark_gui)

# ==== Start GUI ====
root.mainloop()
