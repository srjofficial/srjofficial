import sys
import cv2
import numpy as np
from PIL import Image
import rembg
import io

def prep_photo(input_path, output_path="source-prepped.png"):
    print(f"Processing {input_path}...")
    
    # Read the input image using PIL
    with open(input_path, 'rb') as f:
        input_data = f.read()
        
    # Remove background
    print("Removing background...")
    subject_data = rembg.remove(input_data)
    subject_img = Image.open(io.BytesIO(subject_data)).convert("RGBA")
    
    # Composite onto pure white
    print("Compositing onto white background...")
    white_bg = Image.new("RGBA", subject_img.size, (255, 255, 255, 255))
    composited = Image.alpha_composite(white_bg, subject_img).convert("L")
    
    # Convert to OpenCV format (numpy array) for CLAHE
    img_cv = np.array(composited)
    
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    print("Applying CLAHE...")
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced_cv = clahe.apply(img_cv)
    
    # Save the result
    enhanced_img = Image.fromarray(enhanced_cv)
    enhanced_img.save(output_path)
    print(f"Saved prepped photo to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prep_photo.py <source-photo.jpg>")
        sys.exit(1)
        
    prep_photo(sys.argv[1])
