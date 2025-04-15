from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class AgentCreate(BaseModel):
    name: str
    desc: str
    prompt: str

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    desc: Optional[str] = None
    prompt: Optional[str] = None
    updated_at: Optional[datetime] = None

class AgentOut(AgentCreate):
    id: int
    is_deleted: bool

    class Config:
        from_attributes = True