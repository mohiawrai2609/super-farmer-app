import requests
import os

url = "https://cdn-icons-png.flaticon.com/512/427/427112.png" # Simple transparent sprinkler icon
output_path = "assets/irrigation_hub_clean.png"

try:
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        print(f"Successfully downloaded to {output_path}")
    else:
        # Fallback to a simpler icon if this fails
        fallback_url = "https://img.icons8.com/fluency/96/sprinkler.png"
        r2 = requests.get(fallback_url)
        with open(output_path, 'wb') as f:
            f.write(r2.content)
        print(f"Downloaded fallback to {output_path}")
except Exception as e:
    print(f"Error: {e}")
