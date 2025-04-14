from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import file as file_service
from app.schemas import FileCreate, FileOut
from typing import List

router = APIRouter(prefix="/file", tags=["文件接口"])

@router.post("/", summary="上传文件", response_model=FileOut)
def create_file(payload: FileCreate, db: Session = Depends(get_db)):
    return file_service.create_file(db, **payload.model_dump())

@router.get("/{file_id}", summary="获取文件", response_model=FileOut)
def get_file(file_id: int, db: Session = Depends(get_db)):
    file = file_service.get_file(db, file_id)
    if not file:
        raise HTTPException(404, detail="文件不存在")
    return file

@router.get("/agent/{agent_id}", summary="获取Agent文件列表", response_model=List[FileOut])
def list_files(agent_id: int, db: Session = Depends(get_db)):
    return file_service.list_files_by_agent(db, agent_id)

@router.delete("/{file_id}", summary="删除文件")
def delete_file(file_id: int, db: Session = Depends(get_db)):
    file = file_service.delete_file(db, file_id)
    if not file:
        raise HTTPException(404, detail="文件不存在")
    return {"msg": "文件已删除"}