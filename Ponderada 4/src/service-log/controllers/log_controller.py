from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from services.log_service import create_log, get_logs
from database import get_db

router = APIRouter()

class LogEntry(BaseModel):
    level: str
    message: str

@router.post("/logs")
def create_log_entry(log_entry: LogEntry, db: Session = Depends(get_db)):
    return create_log(db, log_entry.level, log_entry.message)

@router.get("/logs")
def read_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_logs(db, skip, limit)
