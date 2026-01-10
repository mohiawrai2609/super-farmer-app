
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

try:
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    print("Listing available models...")
    # The new SDK list_models might return an iterator
    for m in client.models.list(config={"page_size": 100}):
        print(f"Model: {m.name}")
        if 'generateContent' in m.supported_generation_methods:
             print(f" - Supports generateContent")
except Exception as e:
    print(f"Error: {e}")
