from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import user as user_service
from app.schemas import UserCreate, UserUpdate, UserOut

router = APIRouter(prefix="/user", tags=["用户接口"])

@router.post("/", summary="创建用户", response_model=UserOut)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, **payload.model_dump())

@router.get("/{user_id}", summary="获取用户", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(404, detail="用户不存在")
    return user

@router.put("/{user_id}", summary="更新用户登录信息", response_model=UserOut)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = user_service.update_user(db, user_id, payload)
    if not user:
        raise HTTPException(404, detail="用户不存在")
    return user

@router.delete("/{user_id}", summary="删除用户")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.delete_user(db, user_id)
    if not user:
        raise HTTPException(404, detail="用户不存在")
    return {"msg": "用户已删除"}