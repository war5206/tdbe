from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class SessionCreate(BaseModel):
    user_id: int
    agent_id: int
    document_ids: Optional[str] = None
    title: str

class SessionUpdate(BaseModel):
    document_ids: Optional[str] = None
    title: Optional[str] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SessionOut(SessionCreate):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    class Config:
        from_attributes = True