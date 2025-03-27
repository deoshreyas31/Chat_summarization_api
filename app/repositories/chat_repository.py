from app.database import chats_collection  # Import MongoDB collection
from app.models import ChatMessage
from pymongo.results import DeleteResult
from bson import ObjectId
from datetime import datetime


### ✅ Fetch paginated chat history for a user
async def get_user_chat_history(user_id: str, page: int = 1, limit: int = 10):
    skip = (page - 1) * limit

    chats_cursor = (
        chats_collection.find({"user_id": user_id})
        .sort("timestamp", -1)
        .skip(skip)
        .limit(limit)
    )
    chats = await chats_cursor.to_list(length=limit)

    # ✅ Use count_documents() for accurate filtering
    total_chats = await chats_collection.count_documents({"user_id": user_id})

    return {
        "user_id": user_id,
        "total_chats": total_chats,
        "page": page,
        "limit": limit,
        "messages": [{**chat, "_id": str(chat["_id"])} for chat in chats]  # Convert `_id` to string
    }


### ✅ Store chat message (individual)
async def store_chat(chat: ChatMessage):
    chat_data = chat.dict()
    chat_data["_id"] = str(ObjectId())  # Generate unique ID
    result = await chats_collection.insert_one(chat_data)
    return str(result.inserted_id)


### ✅ Retrieve all chats in a conversation
async def get_chats_by_conversation(conversation_id: str):
    chats_cursor = chats_collection.find({"conversation_id": conversation_id}).sort("timestamp", 1)
    chats = await chats_cursor.to_list(length=None)
    
    return [{**chat, "_id": str(chat["_id"])} for chat in chats]  # Convert `_id` to string


### ✅ Delete all messages in a conversation
async def delete_chat_conversation(conversation_id: str) -> bool:
    result: DeleteResult = await chats_collection.delete_many({"conversation_id": conversation_id})
    return result.deleted_count > 0  # Returns True if at least one document was deleted


from app.database import get_database  # ✅ Import database connection
db = get_database()  # ❌ But `get_database()` returns a string!

async def get_chat_messages(conversation_id: str):
    messages_cursor = db.chats.find({"conversation_id": conversation_id})  # ❌ This will fail!
    messages = await messages_cursor.to_list(length=None)
    return messages



### ✅ Store real-time chat messages (WebSockets / API)
async def store_chat_message(conversation_id: str, user_id: str, message: str):
    chat_doc = {
        "conversation_id": conversation_id,
        "user_id": user_id,
        "message": message,
        "timestamp": datetime.utcnow()
    }
    await chats_collection.insert_one(chat_doc)
