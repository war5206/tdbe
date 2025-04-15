from sqlalchemy import Boolean, Column, BigInteger, DateTime, String, Text
from app.models.base import Base

class Agents(Base):
    __tablename__ = 'agents'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100))
    desc = Column(String(100))
    prompt = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_deleted = Column(Boolean, default=False)