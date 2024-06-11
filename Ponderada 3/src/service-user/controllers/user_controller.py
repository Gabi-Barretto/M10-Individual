from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from services.user_service import create_user, login_user, get_user_by_email
from database import get_db

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, username=user.username, email=user.email, password=user.password)

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    token = login_user(db, username=user.username, password=user.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return token
