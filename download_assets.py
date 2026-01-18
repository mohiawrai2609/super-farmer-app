import requests
import os
from PIL import Image, ImageDraw, ImageFont

# Manually verified high-quality URLs from Browser Subagent
urls = {
    # Existing good ones
    "govt_india.png": "https://cdn-icons-png.flaticon.com/512/924/924915.png",
    
    # New verified URLs
    "iffco.png": "https://upload.wikimedia.org/wikipedia/en/thumb/0/05/Indian_Farmers_Fertiliser_Cooperative_Logo.svg/250px-Indian_Farmers_Fertiliser_Cooperative_Logo.svg.png",
    "mahindra.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Mahindra_Rise_New_Logo.svg/512px-Mahindra_Rise_New_Logo.svg.png",
    "bayer.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Logo_Bayer.svg/512px-Logo_Bayer.svg.png",
    "john_deere.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Logo_John_Deere.svg/512px-Logo_John_Deere.svg.png",
    "syngenta.png": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Syngenta_Logo.svg/250px-Syngenta_Logo.svg.png",
    "upl.png": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b9/UPL_official_logo.svg/250px-UPL_official_logo.svg.png",
    
    # Hard-to-find ones sourced directly
    "nuziveedu.png": "https://pnghdpro.com/wp-content/themes/pnghdpro/download/social-media-and-brands/nuziveedu-seeds-logo.png",
    "jain_irrigation.png": "https://companieslogo.com/img/orig/JISLDVREQS.NS_BIG-724215c3.png"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def generate_fallback_logo(filename, text):
    print(f"⚠️ Generating fallback for {filename}...")
    try:
        img = Image.new('RGB', (512, 512), color="#E0E0E0")
        d = ImageDraw.Draw(img)
        try:
            # Try to load a simpler font or default
            font = ImageFont.load_default()
        except:
            font = None
            
        # Draw text in center
        d.text((50, 256), text, fill="black", font=font)
        img.save(f"assets/{filename}")
    except Exception as e:
        print(f"Failed to generate fallback: {e}")

print("Starting asset download...")
os.makedirs("assets", exist_ok=True)

for name, url in urls.items():
    print(f"Downloading {name} from {url}...")
    try:
        # Stream download to handle larger files better
        r = requests.get(url, headers=headers, timeout=20, stream=True)
        if r.status_code == 200:
            file_path = f"assets/{name}"
            with open(file_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Check if file is valid/non-empty
            if os.path.getsize(file_path) < 100:
                print(f"❌ Failed: {name} (File too small/empty)")
                os.remove(file_path)
                generate_fallback_logo(name, name.split('.')[0])
            else:
                print(f"✅ Success: {name} (Size: {os.path.getsize(file_path)} bytes)")
        else:
            print(f"❌ Failed: {name} (Status: {r.status_code})")
            generate_fallback_logo(name, name.split('.')[0])
            
    except Exception as e:
        print(f"❌ Error downloading {name}: {e}")
        generate_fallback_logo(name, name.split('.')[0])

print("Download complete.")
