from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from . import app, models

def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/logs/")
def create_log(action: str, user_id: int, db: Session = Depends(get_db)):
    db_log = models.Log(action=action, user_id=user_id)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log
