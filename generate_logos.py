from PIL import Image, ImageDraw, ImageFont
import os

def create_logo(name, filename, color):
    # Create simple colored rectangle
    img = Image.new('RGB', (200, 80), color=color)
    d = ImageDraw.Draw(img)
    # Adding text (using default font since custom might not be available)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    d.text((10, 30), name, fill=(255, 255, 255), font=font)
    
    if not os.path.exists('assets'):
        os.makedirs('assets')
    
    img.save(f'assets/{filename}')

# Generate logos
brands = [
    ("Govt of India", "govt_india.png", "#FF9933"), # Saffron
    ("IFFCO", "iffco.png", "#00B050"),
    ("Mahindra", "mahindra.png", "#E31837"),
    ("Bayer", "bayer.png", "#006699"),
    ("John Deere", "john_deere.png", "#367C2B"),
    ("Syngenta", "syngenta.png", "#009374"),
    ("UPL", "upl.png", "#F26522"),
    ("Nuziveedu", "nuziveedu.png", "#00A651"),
    ("Jain Irrigation", "jain_irrigation.png", "#008000")
]

for name, filename, color in brands:
    create_logo(name, filename, color)

print("All brand logos generated successfully in assets/")
