from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChatMessageCreate(BaseModel):
    session_id: int
    message_index: int
    role: str  # 'user' | 'assistant'
    type: str  # 'message' | 'reasoning' | 'system'
    content: str
    reasoning_content: Optional[str] = None

class ChatMessageOut(ChatMessageCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True