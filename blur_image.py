from PIL import Image, ImageFilter
import os

try:
    # Path to the source image
    source_path = os.path.join("assets", "irrigation_bg_v2.png")
    dest_path = os.path.join("assets", "irrigation_bg_blurred.png")
    
    print(f"Opening {source_path}...")
    img = Image.open(source_path)
    
    # Apply Blur
    print("Applying blur...")
    blurred_img = img.filter(ImageFilter.GaussianBlur(radius=5)) # 5px blur is usually good for "little blur"
    
    # Save
    print(f"Saving to {dest_path}...")
    blurred_img.save(dest_path)
    print("Done!")
except Exception as e:
    print(f"Error: {e}")
