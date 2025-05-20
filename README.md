# Image Steganography GUI (COM310006 - Computer Vision Assignment)

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
git clone https://github.com/afiqismail01/com310006_assignment.git
```
2. **Setup Project Environment:**
Open project in PyCharm (preferred), setup virtual environment & install necessary modules in the package.

2. **Run GUI Simulation:**
Find a file named `stagenography_gui.py` in the package and run the file. `(CTRL+SHIFT+F10)`

    ![image](https://github.com/user-attachments/assets/19c6388c-43fe-48e2-9a8a-a286944af6df)

Simulation Video can be found here: https://youtu.be/uZoSPnXC4oc

## Helper Functions:

1. A 3x3 binary watermark image generator can be found in the utils  `watermark_generator.py`. Simply hardcode the values in the matrix with either `0` or `255`  and run the program. `(CTRL+SHIFT+F10)`
    
    ![image](https://github.com/user-attachments/assets/6bea3ac4-b11a-4553-a944-b3302aae350c)
