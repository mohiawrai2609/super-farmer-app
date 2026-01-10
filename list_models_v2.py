
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: GOOGLE_API_KEY not found in environment variables.")
else:
    try:
        client = genai.Client(api_key=api_key)
        print("Listing models...")
        # The SDK might expose models differently. Let's try the common way for this SDK.
        # Based on recent SDK docs, it might be client.models.list()
        
        for m in client.models.list():
            print(f"Model: {m.name} - Display: {m.display_name}")
            
    except Exception as e:
        print(f"Error listing models: {e}")
