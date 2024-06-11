from sqlalchemy.orm import Session
from app.models.log_model import Log

def create_log(db: Session, level: str, message: str):
    log_entry = Log(level=level, message=message)
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry

def get_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Log).offset(skip).limit(limit).all()
