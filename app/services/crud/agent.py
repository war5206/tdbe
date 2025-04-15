from datetime import datetime
from sqlalchemy.orm import Session
from app.models.agents import Agents
from app.schemas import AgentUpdate

def create_agent(db: Session, name: str, desc: str, prompt: str):
    now = datetime.now()
    agent = Agents(
        name=name,
        prompt=prompt,
        desc=desc,
        created_at=now,
        updated_at=now,
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent

def get_agent(db: Session, agent_id: int):
    return db.query(Agents).filter(Agents.id == agent_id, Agents.is_deleted == False).first()

def list_agents(db: Session):
    return db.query(Agents).filter(Agents.is_deleted == False).all()

def update_agent(db: Session, agent_id: int, payload: AgentUpdate):
    agent = db.query(Agents).filter(Agents.id == agent_id, Agents.is_deleted == False).first()
    if agent:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(agent, field, value)
        agent.updated_at = datetime.now()
        db.commit()
        db.refresh(agent)
    return agent

def delete_agent(db: Session, agent_id: int):
    agent = db.query(Agents).filter(Agents.id == agent_id).first()
    if agent:
        agent.is_deleted = True
        db.commit()
    return agent