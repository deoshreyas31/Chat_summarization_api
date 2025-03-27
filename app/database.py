import motor.motor_asyncio
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
load_dotenv()  # Load environment variables

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# Initialize MongoDB client
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
database = client[DB_NAME]

# Collections
chats_collection = database.get_collection("chats")  # Stores chat messages
 

def get_database():
    return database  # ✅ Return the actual database instance
  # ✅ Return the database instance