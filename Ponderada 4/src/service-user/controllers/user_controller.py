from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from services.user_service import create_user, login_user, get_user_by_email, get_all_users
from database import get_db
import requests

LOG_ENDPOINT = "http://localhost:8004/log/logs" 

def log_usage(level: str, message: str):
    try:
        response = requests.post(LOG_ENDPOINT, json={"level": level, "message": message})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to log usage: {e}")


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
    result = create_user(db, username=user.username, email=user.email, password=user.password)
    log_usage(level="INFO", message=f"User registered: {user.email}")
    return result

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    token = login_user(db, username=user.username, password=user.password)
    if not token:
        log_usage(level="WARN", message=f"Failed login attempt: {user.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    log_usage(level="INFO", message=f"User logged in: {user.username}")
    return token

@router.get("/all")
def get_all_users_endpoint(db: Session = Depends(get_db)):
    users = get_all_users(db)
    log_usage(level="INFO", message="Fetched all users")
    return users
