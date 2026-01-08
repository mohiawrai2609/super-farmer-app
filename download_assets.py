
import requests
import os

os.makedirs("assets", exist_ok=True)

urls = {
    "syngenta.png": "https://logo.clearbit.com/syngenta.com",
    "bayer.png": "https://logo.clearbit.com/bayer.com",
    "upl.png": "https://logo.clearbit.com/upl-ltd.com",
    "dhanuka.png": "https://logo.clearbit.com/dhanuka.com" 
}
# Replaced tata with Dhanuka or just use Tata if we have it. Let's try these.

for name, url in urls.items():
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if r.status_code == 200:
            with open(f"assets/{name}", "wb") as f:
                f.write(r.content)
            print(f"Downloaded {name}")
        else:
            print(f"Failed {name}: {r.status_code}")
    except Exception as e:
        print(f"Error {name}: {e}")
