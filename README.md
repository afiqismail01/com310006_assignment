# Image Steganography GUI (COM31006 - Computer Vision Assignment)

This assignment developed an image steganography visualisation tool for embedding a carrier image with watermarks. The tool primarily use SIFT algorithm to detect keypoints and modify the image bit values using Least Significant Bit (LSB). 
Designed as part of the COM310006 assignment.

---

## Features / Workflow

Watermark Embedder:
- Input Images & Preprocessing
- Keypoint Detection with SIFT
- Watermark Encoding (binarise) & Embedding

Watermark Recovery:
- Re-apply SIFT algorithm to detect **same** keypoints
- verify image authenticity by checking the watermark presence
  
Tampering Detector:
- Input image for testing by comparing watermark consistency
- Built-in tampering techniques (cropping 20% & rotating)
- Analysis section for the input image
---

## How to Run Simulation

1. **Clone project:**

```bash
git clone https://github.com/afiqismail01/com31006_assignment.git
```
2. **Setup Project Environment:**
Open project in PyCharm (preferred) with `Python3.13`, setup virtual environment & install packages below:

  ```bash
  # Create a new virtual environment in a folder called "venv"
  python -m venv .venv
  
  # Activate the virtual environment (Windows)
  .\.venv\Scripts\activate
  
  # Install required packages
  pip install numpy opencv-python pillow
  ```

3. **Sample Carrier Image & Watermarks :**
    - CARRIER IMAGE: carrier_image.png
    - WATERMARK: watermark_1.png, watermark_2.png & watermark_3.png
    - EMBEDDED IMAGE: watermarked_output.png
    - TAMPERED IMAGE: watermarked_rotated_output.png & watermarked_cropped_image.png (need to be generated using buttons in Frame 6 GUI)
    - TEST IMAGE: use any image from your local device to perform testing
4. **Run GUI Simulation:**
Find a file named `stagenography_gui.py` in the package and run the file. `(CTRL+SHIFT+F10)`

    ![image](https://github.com/user-attachments/assets/19c6388c-43fe-48e2-9a8a-a286944af6df)

Simulation Video can be found here: https://youtu.be/uZoSPnXC4oc

## Helper Functions & Extras:

1. A 3x3 binary watermark image generator can be found in the utils  `watermark_generator.py`. Simply hardcode the values in the matrix with either `0` or `255`  and run the program. `(CTRL+SHIFT+F10)`
    
    ![image](https://github.com/user-attachments/assets/6bea3ac4-b11a-4553-a944-b3302aae350c)

