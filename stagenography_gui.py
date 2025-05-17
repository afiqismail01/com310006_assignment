import cv2
import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk
from tkinter import messagebox
from SIFT_detector_1 import detect_sift_keypoints
from embed_watermark_2 import embed_watermark

# Global reference to the label and image
image_label = None
image_tk = None  # To prevent garbage collection

carrier_path = None
watermark_path = None
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
    global watermark_path
    path = filedialog.askopenfilename(title="Select Watermark Image")
    if path:
        watermark_path = path
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


root = tk.Tk()
root.title("Watermark Steganography GUI")
root.geometry("400x500")

# Image display label
image_label = tk.Label(root)
image_label.pack()

# Button
load_btn = tk.Button(root, text="Load Carrier Image", command=load_carrier)
load_btn.pack(pady=10)
load_wm_btn = tk.Button(root, text="Load Watermark Image", command=load_watermark)
load_wm_btn.pack(pady=10)
embed_btn = tk.Button(root, text="Embed Watermark", command=embed_watermark_gui)
embed_btn.pack(pady=10)



root.mainloop()
