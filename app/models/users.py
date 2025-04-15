from sqlalchemy import Boolean, Column, BigInteger, ForeignKey, String, DateTime
from app.models.base import Base

class UsersLogin(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    
    username = Column(String(100), unique=True, nullable=False)
    telephone = Column(String(20), unique=True, nullable=False)
    password = Column(String(64), nullable=False)

    department_level1 = Column(String(100))
    department_level2 = Column(String(100))
    position = Column(String(100))

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    is_deleted = Column(Boolean, default=False)