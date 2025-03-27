import openai
import os
import nltk
import nltk
from typing import List

nltk.download("punkt")
from nltk.tokenize import word_tokenize  # Ensure it's imported

from textblob import TextBlob
from collections import Counter
from dotenv import load_dotenv

load_dotenv()  # Load API key from .env file

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Store API Key in .env

nltk.download("punkt")  # Download NLP tokenizer

async def analyze_sentiment(text: str) -> str:
    """
    Perform sentiment analysis using TextBlob.
    Returns: "Positive", "Negative", or "Neutral"
    """
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

async def extract_keywords(text: str) -> list:
    """
    Extract the most common keywords from the text.
    """
    words = word_tokenize(text.lower())  # ✅ Use `word_tokenize`

    common_words = ["is", "the", "a", "to", "and", "of", "in", "for", "on", "with", "that", "it"]  # Stopwords
    filtered_words = [word for word in words if word.isalnum() and word not in common_words]
    keyword_counts = Counter(filtered_words)
    return [word for word, _ in keyword_counts.most_common(5)]  # Return top 5 keywords

async def classify_topic(text: str) -> str:
    """
    Use OpenAI to classify the topic of the conversation.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"Classify this conversation into a topic: {text}"}],
            max_tokens=10
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error in topic classification: {str(e)}"

async def analyze_chat(conversation_id: str, messages: List[str]):

    """
    Perform sentiment analysis, keyword extraction, and topic classification on a conversation.
    """
    if not messages:
        return {"error": "No chat messages available for analysis."}

    full_text = " ".join(messages)  # Merge messages into one text block

    sentiment = await analyze_sentiment(full_text)
    keywords = await extract_keywords(full_text)
    topic = await classify_topic(full_text)

    return {
        "conversation_id": conversation_id,
        "sentiment": sentiment,
        "keywords": keywords,
        "topic": topic
    }
