from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from . import app, models

def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/")
def create_user(username: str, password: str, db: Session = Depends(get_db)):
    db_user = models.User(username=username, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
