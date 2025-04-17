from sqlalchemy.orm import Session
from app.models.sessions import ChatMessages
from datetime import datetime

def create_message(db: Session, session_id: int, message_index: int, role: str, type: str, content: str):
    message = ChatMessages(
        session_id=session_id,
        message_index=message_index,
        role=role,
        type=type,
        content=content,
        created_at=datetime.now(),
        is_deleted=False
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

def get_messages_by_session(db: Session, session_id: int):
    return db.query(ChatMessages).filter(ChatMessages.session_id == session_id, ChatMessages.is_deleted == False).order_by(ChatMessages.message_index).all()

def delete_message(db: Session, message_id: int):
    message = db.query(ChatMessages).filter(ChatMessages.id == message_id).first()
    if message:
        message.is_deleted = True
        db.commit()
    return message