from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    telephone: str
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    telephone: Optional[str] = None
    password: Optional[str] = None  # 将被自动 SHA256 加密处理

class UserOut(BaseModel):
    id: int
    username: str
    telephone: str
    created_at: datetime

    class Config:
        from_attributes = True