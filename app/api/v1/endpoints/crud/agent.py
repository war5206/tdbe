from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import agent as agent_service
from app.schemas import AgentCreate, AgentUpdate ,AgentOut
from typing import List

router = APIRouter(prefix="/agent", tags=["阿里云AI应用接口"])

@router.post("/", summary="创建Agent", response_model=AgentOut)
def create_agent(payload: AgentCreate, db: Session = Depends(get_db)):
    return agent_service.create_agent(db, **payload.model_dump())

@router.get("/{agent_id}", summary="获取Agent", response_model=AgentOut)
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    agent = agent_service.get_agent(db, agent_id)
    if not agent:
        raise HTTPException(404, detail="Agent不存在")
    return agent

@router.get("/", summary="Agent列表", response_model=List[AgentOut])
def list_agents(db: Session = Depends(get_db)):
    return agent_service.list_agents(db)

@router.put("/{agent_id}", summary="更新agent信息", response_model=AgentUpdate)
def update_agent(agent_id: int, payload: AgentUpdate, db: Session = Depends(get_db)):
    agent = agent_service.update_agent(db, agent_id, payload)
    if not agent:
        raise HTTPException(404, detail="agent不存在")
    return agent

@router.delete("/{agent_id}", summary="删除Agent")
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    agent = agent_service.delete_agent(db, agent_id)
    if not agent:
        raise HTTPException(404, detail="Agent不存在")
    return {"msg": "Agent已删除"}