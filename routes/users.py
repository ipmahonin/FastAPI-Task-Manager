#код из routes.users.py
from fastapi import APIRouter, Depends
from service.user_service import register, login
from schemas.user import UserCreate,UserLogin,RefreshRequest
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from service.user_service import SECRET_KEY, ALGORITHM
from service.user_service import create_access_token
router = APIRouter()

@router.post('/register', status_code=201)
def add_user_app(user: UserCreate):
    result = register(user)
    if result is None:
        raise HTTPException(status_code=401,detail='Invalid user register')
    return result

@router.post('/login')
def login_user_app(form_data: OAuth2PasswordRequestForm = Depends()):
    user = UserLogin(
        email=form_data.username,
        password=form_data.password
    )
    result = login(user)
    if result is None:
        raise HTTPException(status_code=401, detail='Invalid user login')
    return result

@router.post('/refresh')
def refresh_token(refresh_token_get:RefreshRequest):
    try:
        payload = jwt.decode(refresh_token_get.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")
    user_id = payload.get("user_id")
    new_access = create_access_token(user_id)

    return {
        "access_token": new_access,
        "token_type": "bearer"
    }