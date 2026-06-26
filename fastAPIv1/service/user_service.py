#код из service.user_service.py
from schemas.user import UserCreate, UserLogin
from repository.user_repository import add_user,get_user_by_email
from db import SessionLocal
import bcrypt
from jose import jwt
from datetime import datetime,timedelta,timezone
from fastapi import HTTPException
from core.logger import logger

SECRET_KEY = "secret"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 1

def hash_password(password: str):
    password_bytes=password.encode('utf-8')
    salt=bcrypt.gensalt()
    hashed=bcrypt.hashpw(password_bytes,salt)
    return hashed.decode('utf-8')

def verify_password(password:str,hashed_password:str):
    password_bytes  = password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes,hashed_bytes)

def create_access_token(user_id:int):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "user_id": user_id,
        "type": "access",
        "exp": expire
        }
    token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return token

def create_refresh_token(user_id:int):
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload = {
        'user_id':user_id,
        'type':'refresh',
        'exp':expire
    }
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

def register(user: UserCreate):
    db=SessionLocal()
    result = get_user_by_email(db=db,email=user.email)
    if result is not None:
        db.close()
        logger.error(f"User register error. User {user.email} already exists")
        raise HTTPException(status_code=400, detail="User already exists")
    hashed=hash_password(password=user.password)
    try:
        result=add_user(db,user.email,hashed)
        logger.info(f"User {user.email} register.")
        return {
    "id": result.id,
    "email": result.email
            }
    finally:
        db.close()

def login(user: UserLogin):
    db = SessionLocal()
    try:
        db_user = get_user_by_email(db=db, email=user.email)
        if (db_user is None) or not verify_password(user.password, db_user.password_hash):
            logger.warning(f"Login failed for {user.email}")
            raise HTTPException(status_code=401, detail="Invalid credentials")
        access = create_access_token(db_user.id)
        refresh = create_refresh_token(db_user.id)
        logger.info(f"User {user.email} logged in")
        return {
            "access_token": access,
            "refresh_token": refresh,
            "token_type": "bearer"
        }
    finally:
        db.close()
