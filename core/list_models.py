import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("✅ Gemini client initialized successfully\n")
print("Available models for this API key:\n")

for model in client.models.list():
    print(f"- {model.name}")
