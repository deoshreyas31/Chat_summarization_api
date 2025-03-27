from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Chat Message Schema
class ChatMessage(BaseModel):
    user_id: str  # Unique user identifier
    conversation_id: str  # Unique conversation identifier
    message: str  # Chat message content
    timestamp: Optional[datetime] = datetime.utcnow()  # Auto-generate timestamp
