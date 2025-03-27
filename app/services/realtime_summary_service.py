import openai
import os
from dotenv import load_dotenv
from app.repositories.chat_repository import store_chat_message

load_dotenv()  # Load OpenAI API Key

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Store API Key in .env

async def generate_summary(messages: list) -> str:
    """
    Generate a real-time summary using OpenAI's GPT-4.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"Summarize this conversation: {messages}"}],
            max_tokens=100
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error generating summary: {str(e)}"

async def process_chat(conversation_id: str, user_id: str, message: str, messages: list):
    """
    Store the message and generate a summary.
    """
    await store_chat_message(conversation_id, user_id, message)
    summary = await generate_summary(messages)
    return summary
