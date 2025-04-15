from sqlalchemy.orm import Session
from app.models.files import Files
from datetime import datetime

def create_file(db: Session, name: str, file_path: str, agent_id: int, session_id: int, message_id: int, uploaded_by: int):
    file = Files(
        name=name,
        file_path=file_path,
        agent_id=agent_id,
        session_id=session_id,
        message_id=message_id,
        uploaded_by=uploaded_by
    )
    db.add(file)
    db.commit()
    db.refresh(file)
    return file

def get_file(db: Session, file_id: int):
    return db.query(Files).filter(Files.id == file_id, Files.is_deleted == False).first()

def list_files_by_agent(db: Session, agent_id: int):
    return db.query(Files).filter(Files.agent_id == agent_id, Files.is_deleted == False).all()

def delete_file(db: Session, file_id: int):
    file = db.query(Files).filter(Files.id == file_id).first()
    if file:
        file.is_deleted = True
        db.commit()
    return file