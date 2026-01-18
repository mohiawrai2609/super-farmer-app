from rembg import remove
from PIL import Image
import os

input_path = "assets/irrigation_hub_v2.png"
output_path = "assets/irrigation_hub_final.png"

if os.path.exists(input_path):
    print(f"Processing {input_path}...")
    try:
        input_image = Image.open(input_path)
        output_image = remove(input_image)
        output_image.save(output_path)
        print(f"Saved background-removed image to {output_path}")
    except Exception as e:
        print(f"Error removing background: {e}")
else:
    print(f"Input file not found: {input_path}")
