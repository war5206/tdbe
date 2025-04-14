from sqlalchemy.orm import Session
from app.models.agents import Agents

def create_agent(db: Session, name: str, prompt: str, agent_api_key: str, app_id: str, pipeline_ids: str):
    agent = Agents(name=name, prompt=prompt, agent_api_key=agent_api_key, app_id=app_id, pipeline_ids=pipeline_ids)
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent

def get_agent(db: Session, agent_id: int):
    return db.query(Agents).filter(Agents.id == agent_id, Agents.is_deleted == False).first()

def list_agents(db: Session):
    return db.query(Agents).filter(Agents.is_deleted == False).all()

def delete_agent(db: Session, agent_id: int):
    agent = db.query(Agents).filter(Agents.id == agent_id).first()
    if agent:
        agent.is_deleted = True
        db.commit()
    return agent