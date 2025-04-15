from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    telephone: str
    password: str
    department_level1: str
    department_level2: str
    position: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    telephone: Optional[str] = None
    password: Optional[str] = None  # 将被自动 SHA256 加密处理
    department_level1: Optional[str] = None
    department_level2: Optional[str] = None
    position: Optional[str] = None
    updated_at: Optional[datetime] = None

class UserOut(BaseModel):
    id: int
    username: str
    telephone: str
    department_level1: str
    department_level2: str
    position: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True