from sqlalchemy.orm import Session
from models.log_model import Log
import datetime

def create_log(db: Session, level: str, message: str):
    log = Log(level=level, message=message, timestamp=datetime.datetime.utcnow())
    db.add(log)
    db.commit()
    db.refresh(log)
    # Escreve no arquivo de log
    with open("/var/log/app_logs.log", "a") as log_file:
        log_file.write(f"{log.timestamp} - {log.level} - {log.message}\n")
    return log

def get_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Log).offset(skip).limit(limit).all()
