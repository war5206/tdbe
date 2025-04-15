from sqlalchemy.orm import Session
from app.models.sessions import ChatSessions
from app.schemas import SessionCreate, SessionUpdate
from datetime import datetime

def create_session(db: Session, user_id: int, agent_id: int, document_ids: str, title: str):
    now = datetime.now()
    session = ChatSessions(
        user_id=user_id,
        agent_id=agent_id,
        document_ids=document_ids,
        title=title,
        created_at=now,
        updated_at=now,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def get_session(db: Session, session_id: int):
    return db.query(ChatSessions).filter(ChatSessions.id == session_id, ChatSessions.is_deleted == False).first()

def list_sessions_by_user(db: Session, user_id: int):
    return db.query(ChatSessions).filter(ChatSessions.user_id == user_id, ChatSessions.is_deleted == False).all()

def update_session(db: Session, user_id: int, session_id: int, payload: SessionUpdate):
    session = db.query(ChatSessions).filter(ChatSessions.id == session_id, ChatSessions.user_id == user_id, ChatSessions.is_deleted == False).first()
    if session:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(session, field, value)
        session.updated_at = datetime.now()
        db.commit()
        db.refresh(session)
    return session

def delete_session(db: Session, session_id: int):
    session = db.query(ChatSessions).filter(ChatSessions.id == session_id).first()
    if session:
        session.is_deleted = True
        db.commit()
    return session