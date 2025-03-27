from fastapi import APIRouter, HTTPException, Query, Depends
from app.models import ChatMessage
import app.repositories.chat_repository as repo
from app.services.summarization_service import summarize_chat
from app.services.insights_service import analyze_chat
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from app.repositories.chat_repository import get_chat_messages  # ✅ Import function
from app.services.summarization_service import summarize_chat  

router = APIRouter()

# ✅ Test API Route
@router.get("/test")
async def test_route():
    return {"message": "Chats API is working!"}

# ✅ Store a New Chat Message
@router.post("/chats", response_model=dict)
async def create_chat(chat: ChatMessage):
    """
    Store a new chat message in MongoDB.
    """
    try:
        chat_id = await repo.store_chat(chat)
        return {"message": "Chat stored successfully!", "chat_id": chat_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Retrieve All Messages in a Conversation
@router.get("/chats/{conversation_id}", response_model=dict)
async def get_chats(conversation_id: str):
    """
    Retrieve all messages for a given conversation ID.
    """
    try:
        chats = await repo.get_chats_by_conversation(conversation_id)
        if not chats:
            raise HTTPException(status_code=404, detail="No chats found for this conversation ID")
        return {"conversation_id": conversation_id, "messages": chats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Paginated Chat History for a User
@router.get("/users/{user_id}/chats", response_model=dict)
async def get_user_chats(
    user_id: str,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    """
    Fetch paginated chat history for a user.
    """
    try:
        chat_history = await repo.get_user_chat_history(user_id, page, limit)
        if not chat_history["messages"]:
            raise HTTPException(status_code=404, detail="No chat history found for this user.")
        return chat_history
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Delete a Conversation
@router.delete("/chats/{conversation_id}")
async def delete_chat(conversation_id: str):
    """
    Delete all messages in a conversation.
    """
    try:
        deleted = await repo.delete_chat_conversation(conversation_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Conversation not found.")
        return {"message": "Conversation deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Summarize a Conversation
@router.post("/chats/summarize")
async def summarize_chat_api(conversation_id: str):
    """
    Summarize a conversation using an LLM.
    """
    try:
        messages = await get_chat_messages(conversation_id)  # ✅ Correct function usage
        if not messages:
            raise HTTPException(status_code=404, detail="No messages found for this conversation.")

        summary = await summarize_chat( messages)  # ✅ Fixed function call
        return {"conversation_id": conversation_id, "summary": summary}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Analyze a Chat Conversation (Sentiment, Keywords, Topics)
class AnalyzeRequest(BaseModel):
    conversation_id: str

@router.post("/chats/analyze")
async def analyze_chat_api(request: AnalyzeRequest):
    try:
        messages = await repo.get_chat_messages(request.conversation_id)
        print(f"DEBUG: Retrieved messages from DB: {messages}")  # 🔍 Debugging log

        if not messages or len(messages) == 0:
            raise HTTPException(status_code=404, detail="No chat messages available for analysis.")

        # Extract messages from chat logs
        message_texts = [msg["message"] for msg in messages if isinstance(msg, dict) and "message" in msg]
        if not messages or not isinstance(messages, list):
            raise HTTPException(status_code=404, detail="No chat messages available for analysis.")

        print(f"DEBUG: Extracted messages for analysis: {message_texts}")  # 🔍 Debugging log

        insights = await analyze_chat(request.conversation_id, message_texts)
        return insights
    except Exception as e:
        print(f"ERROR: {e}")  # 🔍 Print exact error
        raise HTTPException(status_code=500, detail=str(e))





