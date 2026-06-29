from dotenv import load_dotenv
import os
from anthropic import Anthropic

# Load environment variables
load_dotenv()

# Read API key
api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not found. Check your .env file.")

# Create client
client = Anthropic(api_key=api_key)

# Call Claude
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=100,
    messages=[
        {
            "role": "user",
            "content": "What is Quantum Computing? Answer in one sentence."
        }
    ]
)

# Print only the generated text
print(response.content[0].text)