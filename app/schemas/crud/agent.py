from pydantic import BaseModel
from datetime import datetime

class AgentCreate(BaseModel):
    name: str
    prompt: str
    agent_api_key: str
    app_id: str
    pipeline_ids: str

class AgentOut(AgentCreate):
    id: int
    is_deleted: bool

    class Config:
        from_attributes = True