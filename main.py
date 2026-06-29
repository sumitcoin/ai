from dotenv import load_dotenv
import openai
import langchain
import os

# Load .env file
load_dotenv()

# Read API key
api_key = os.getenv("OPENAI_API_KEY")

print("Hello Wo")