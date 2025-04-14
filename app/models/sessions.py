from sqlalchemy import Boolean, Column, BigInteger, String, DateTime, ForeignKey, Integer, Text, Enum
from app.models.base import Base, UserRole, MessageType

class ChatSessions(Base):
    __tablename__ = 'chat_sessions'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users_login.id'))
    agent_id = Column(BigInteger, ForeignKey('agents.id'))
    document_ids = Column(String(100))
    title = Column(String(100))
    created_at = Column(DateTime)
    is_deleted = Column(Boolean, default=False)

class ChatMessages(Base):
    __tablename__ = 'chat_messages'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    session_id = Column(BigInteger, ForeignKey('chat_sessions.id'))
    message_index = Column(Integer)
    role = Column(Enum(UserRole))
    type = Column(Enum(MessageType))
    content = Column(Text)
    reasoning_content = Column(Text)
    created_at = Column(DateTime)
    is_deleted = Column(Boolean, default=False)