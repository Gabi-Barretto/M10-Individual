from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.database import get_db
from repositories.user_repository import UserRepository
from services import send_message_rabbitmq, receive_last_message_rabbitmq, Message
from schemas.user_schema import LoginRequest, RegisterRequest
from jose import jwt
import datetime

router = APIRouter()

@router.post("/register", response_class=JSONResponse)
async def register_user(request: RegisterRequest, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    
    if not all([request.name, request.email, request.password]):
        return JSONResponse(status_code=400, content={"message": "Missing data"})
    
    user = user_repo.create_user(request.name, request.email, request.password)
    
    log_message = Message(date=datetime.datetime.now(), msg=f"User {request.email} registered.")
    send_message_rabbitmq(log_message)
    
    return JSONResponse(content={"message": "User registered successfully!"})

@router.post("/login", response_class=JSONResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    
    if not all([request.email, request.password]):
        return JSONResponse(status_code=400, content={"message": "Missing data"})
    
    user = user_repo.get_user_by_email(request.email)
    if not user or user.password != request.password:
        return JSONResponse(status_code=422, content={"message": "Bad username or password"})
    
    access_token = jwt.encode({"sub": user.id}, "goku-vs-vegeta", algorithm="HS256")
    
    log_message = Message(date=datetime.datetime.now(), msg=f"User {request.email} logged in.")
    send_message_rabbitmq(log_message)
    
    return JSONResponse(content={"access_token": access_token})
