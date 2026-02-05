import requests
import os

assets_dir = "assets"
os.makedirs(assets_dir, exist_ok=True)

urls = {
    "video_drone.jpg": "https://loremflickr.com/640/360/drone,agriculture/all",
    "video_sugarcane.jpg": "https://loremflickr.com/640/360/sugarcane,farm/all",
    "video_fertilizer.jpg": "https://loremflickr.com/640/360/soil,plants/all",
    "video_drone2.jpg": "https://loremflickr.com/640/360/tractor,farm/all"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

for filename, url in urls.items():
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        with open(os.path.join(assets_dir, filename), "wb") as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
