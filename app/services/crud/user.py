from datetime import datetime
from sqlalchemy.orm import Session
from app.models.users import UsersLogin
from app.schemas import UserUpdate
import hashlib

def create_user(db: Session, username: str, telephone: str, password: str):
    password = hashlib.sha256(password.encode()).hexdigest() # Hash the password
    user = UsersLogin(username=username, telephone=telephone, password=password, created_at=datetime.now())
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
        db.commit()
        db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(UsersLogin).filter(UsersLogin.id == user_id).first()
    if user:
        user.is_deleted = True
        db.commit()
    return user