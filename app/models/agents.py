from sqlalchemy import Boolean, Column, BigInteger, String, Text
from app.models.base import Base

class Agents(Base):
    __tablename__ = 'agents'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100))
    prompt = Column(Text)
    agent_api_key = Column(String(100))
    app_id = Column(String(100))
    pipeline_ids = Column(String(100))
    is_deleted = Column(Boolean, default=False)