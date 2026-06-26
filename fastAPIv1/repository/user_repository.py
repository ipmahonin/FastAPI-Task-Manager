#код из user_repository.py
from models.user import User
from sqlalchemy.orm import Session

def add_user(db: Session, email: str, password: str):
    user = User(email=email,password_hash=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session,email: str):
    return db.query(User).filter(User.email == email).first()

