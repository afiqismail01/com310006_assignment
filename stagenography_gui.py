import cv2
import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk
from tkinter import messagebox
from SIFT_detector_1 import detect_sift_keypoints
from embed_watermark_2 import embed_watermark
from extract_watermark_3 import extract_watermark_by_coords
from tampering_detector_4 import detect_tampering_by_coords


# Global reference to the label and image
image_label = None
image_tk = None  # To prevent garbage collection

carrier_path = None
watermark_path = None
root = tk.Tk()
root.title("Watermark Steganography GUI")
root.geometry("400x500")

# Image display labels
image_label = tk.Label(root)
image_label.pack()

wm_label = tk.Label(root)  # ✅ Watermark display label
wm_label.pack()

keypoints = None
image = None
embed_locs = []


def load_carrier():
    global carrier_path, keypoints, image, image_tk
    carrier_path = filedialog.askopenfilename(title="Select Carrier Image")
    if carrier_path:
        image, keypoints, _ = detect_sift_keypoints(carrier_path)
        img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)).resize((300, 300))
        image_tk = ImageTk.PhotoImage(img_pil)
        image_label.config(image=image_tk)
        print("Carrier image loaded:", carrier_path)


watermark_path = None  # Global to store the path
def load_watermark():
    global watermark_path, wm_image_tk
    path = filedialog.askopenfilename(title="Select Watermark Image")
    if path:
        watermark_path = path
        img = Image.open(path)
        img = img.resize((100, 100))  # Resize small for UI
        wm_image_tk = ImageTk.PhotoImage(img)
        wm_label.config(image=wm_image_tk)
        messagebox.showinfo("Loaded", "Watermark image loaded.")
        print("Watermark image loaded:", path)


def embed_watermark_gui():
    global image, embed_locs

    if not carrier_path or not watermark_path:
        messagebox.showerror("Error", "Load both carrier and watermark images first.")
        return

    index = simpledialog.askinteger("Keypoint Index", "Enter keypoint index (0-9):", minvalue=0, maxvalue=9)
    if index is None:
        return

    try:
        image, loc = embed_watermark(image, keypoints, watermark_path, index)
        embed_locs = [loc]
        cv2.imwrite("watermarked_output.png", image)

        img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)).resize((300, 300))
        image_tk = ImageTk.PhotoImage(img_pil)
        image_label.config(image=image_tk)

        messagebox.showinfo("Success", f"Watermark embedded at keypoint index {index}.")
    except Exception as e:
        messagebox.showerror("Embedding Failed", str(e))

def detect_tampering_gui():
    global image

    if not embed_locs:
        messagebox.showerror("Error", "No watermark has been embedded yet.")
        return

    if not watermark_path:
        messagebox.showerror("Error", "Watermark image not available for comparison.")
        return

    ref_wm = cv2.imread(watermark_path, cv2.IMREAD_GRAYSCALE)
    tampered = detect_tampering_by_coords(image, embed_locs, ref_wm)

    if not tampered:
        messagebox.showinfo("Result", "✅ No tampering detected.")
    else:
        for (x, y) in tampered:
            cv2.circle(image, (x, y), radius=6, color=(0, 0, 255), thickness=2)

        cv2.imwrite("tampering_detected.png", image)
        img_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)).resize((300, 300))
        img_tk = ImageTk.PhotoImage(img_pil)
        image_label.config(image=img_tk)

        messagebox.showwarning("Tampering", f"⚠️ Tampering detected at: {tampered}")


# Button
load_btn = tk.Button(root, text="Load Carrier Image", command=load_carrier)
load_btn.pack(pady=10)
load_wm_btn = tk.Button(root, text="Load Watermark Image", command=load_watermark)
load_wm_btn.pack(pady=10)
embed_btn = tk.Button(root, text="Embed Watermark", command=embed_watermark_gui)
embed_btn.pack(pady=10)
detect_btn = tk.Button(root, text="Detect Tampering", command=detect_tampering_gui)
detect_btn.pack(pady=10)




root.mainloop()
