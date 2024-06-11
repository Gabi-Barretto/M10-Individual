from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.log_service import create_log, get_logs
from models.log_model import Log
from database import get_db

router = APIRouter()

@router.post("/logs")
def create_log_entry(level: str, message: str, db: Session = Depends(get_db)):
    return create_log(db, level, message)

@router.get("/logs")
def read_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_logs(db, skip, limit)
