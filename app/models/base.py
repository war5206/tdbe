from app.database import Base
from sqlalchemy import Column, BigInteger, String, DateTime, Text, ForeignKey, Enum, Integer
import enum

class UserRole(enum.Enum):
    user = "user"
    assistant = "assistant"

class MessageType(enum.Enum):
    message = "message"
    reasoning = "reasoning"
    system = "system"