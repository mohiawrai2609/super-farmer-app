from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GOOGLE_API_KEY")
print(f"Testing Key: {key}")

try:
    client = genai.Client(api_key=key)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Say hello"
    )
    print("Success!")
    print(response.text)
except Exception as e:
    print("Failed")
    print(e)
