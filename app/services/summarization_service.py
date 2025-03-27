import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load API key from .env file

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Store API Key in .env
openai.api_key = OPENAI_API_KEY  # ✅ Set API Key for OpenAI 0.28

def summarize_chat(messages, model="gpt-4"):  # ✅ Accept two arguments
    response = openai.ChatCompletion.create(
        model=model,  # ✅ Use model argument
        messages=messages
    )
    return response["choices"][0]["message"]["content"]
