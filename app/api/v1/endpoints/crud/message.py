from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import message as message_service
from app.schemas import ChatMessageCreate, ChatMessageOut
from typing import List

router = APIRouter(prefix="/message", tags=["对话接口"])

@router.post("/", summary="添加聊天消息", response_model=ChatMessageOut)
def create_message(payload: ChatMessageCreate, db: Session = Depends(get_db)):
    return message_service.create_message(
        db,
        session_id=payload.session_id,
        message_index=payload.message_index,
        role=payload.role,
        type=payload.type,
        content=payload.content,
        reasoning_content=payload.reasoning_content,
    )

@router.get("/session/{session_id}", summary="获取会话消息", response_model=List[ChatMessageOut])
def get_messages(session_id: int, db: Session = Depends(get_db)):
    return message_service.get_messages_by_session(db, session_id)

@router.delete("/{message_id}", summary="删除消息")
def delete_message(message_id: int, db: Session = Depends(get_db)):
    message = message_service.delete_message(db, message_id)
    if not message:
        raise HTTPException(404, detail="消息不存在")
    return {"msg": "消息已删除"}
