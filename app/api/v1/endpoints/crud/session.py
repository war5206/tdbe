from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import session as session_service
from app.schemas import SessionCreate, SessionOut
from typing import List

router = APIRouter(prefix="/session", tags=["session接口"])

@router.post("/", summary="创建会话", response_model=SessionOut)
def create_session(payload: SessionCreate, db: Session = Depends(get_db)):
    return session_service.create_session(db, **payload.model_dump())

@router.get("/{session_id}", summary="获取会话", response_model=SessionOut)
def get_session(session_id: int, db: Session = Depends(get_db)):
    session = session_service.get_session(db, session_id)
    if not session:
        raise HTTPException(404, detail="会话不存在")
    return session

@router.get("/user/{user_id}", summary="获取用户会话列表", response_model=List[SessionOut])
def list_sessions(user_id: int, db: Session = Depends(get_db)):
    return session_service.list_sessions_by_user(db, user_id)

@router.delete("/{session_id}", summary="删除会话")
def delete_session(session_id: int, db: Session = Depends(get_db)):
    session = session_service.delete_session(db, session_id)
    if not session:
        raise HTTPException(404, detail="会话不存在")
    return {"msg": "会话已删除"}