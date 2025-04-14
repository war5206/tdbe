from sqlalchemy import Boolean, Column, BigInteger, String, Text, ForeignKey
from app.models.base import Base

class Files(Base):
    __tablename__ = 'files'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100))
    file_path = Column(Text)
    agent_id = Column(BigInteger, ForeignKey('agents.id'))
    uploaded_by = Column(BigInteger, ForeignKey('users_login.id'))
    is_deleted = Column(Boolean, default=False)
    message_id = Column(BigInteger, ForeignKey('chat_messages.id'))