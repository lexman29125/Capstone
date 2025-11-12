import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

resp = openai.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Say hello!"}],
    temperature=0
)
print(resp.choices[0].message.content)