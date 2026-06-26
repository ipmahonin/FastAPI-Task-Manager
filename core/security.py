#код из core.security.py
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
from fastapi import HTTPException,Depends
from db import SessionLocal
from service.user_service import SECRET_KEY, ALGORITHM
from repository.user_repository import get_user_by_id


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    db = SessionLocal()
    try:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
        user_id=payload.get('user_id')
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = get_user_by_id(db, user_id)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
        
    finally:
        db.close()