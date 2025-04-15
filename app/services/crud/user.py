from datetime import datetime
from sqlalchemy.orm import Session
from app.models.users import UsersLogin
from app.schemas import UserCreate,UserUpdate
import hashlib

def create_user(db: Session, username: str, telephone: str, password: str, department_level1: str, department_level2: str, position: str):
    password = hashlib.sha256(password.encode()).hexdigest() # Hash the password
    now = datetime.now()
    user = UsersLogin(
        username=username,
        telephone=telephone,
        password=password,
        department_level1=department_level1,
        department_level2=department_level2,
        position=position,
        created_at=now,
        updated_at=now
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, user_id: int):
    return db.query(UsersLogin).filter(UsersLogin.id == user_id).first()

def update_user(db: Session, user_id: int, payload: UserUpdate):
    user = db.query(UsersLogin).filter(UsersLogin.id == user_id, UsersLogin.is_deleted == False).first()
    if user:
        for field, value in payload.model_dump(exclude_unset=True).items():
            if field == "password" and value:
                value = hashlib.sha256(value.encode()).hexdigest()
            setattr(user, field, value)
        user.updated_at = datetime.now()
        db.commit()
        db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(UsersLogin).filter(UsersLogin.id == user_id).first()
    if user:
        user.is_deleted = True
        db.commit()
    return user