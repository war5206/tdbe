from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote_plus

# 数据库创建
# CREATE DATABASE aichat DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

pwd = quote_plus("Solar@3366")
DB_URL = f"mysql+pymysql://root:{pwd}@localhost:3306/aichat"

engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()