from pydantic import BaseModel
from datetime import datetime

class SessionCreate(BaseModel):
    user_id: int
    agent_id: int
    document_ids: str
    title: str

class SessionOut(SessionCreate):
    id: int
    created_at: datetime
    is_deleted: bool

    class Config:
        from_attributes = True