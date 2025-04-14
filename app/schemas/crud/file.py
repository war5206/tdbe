from pydantic import BaseModel
from datetime import datetime

class FileCreate(BaseModel):
    name: str
    file_path: str
    agent_id: int
    uploaded_by: int

class FileOut(FileCreate):
    id: int
    is_deleted: bool

    class Config:
        from_attributes = True