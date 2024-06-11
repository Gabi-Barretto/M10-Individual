from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.utils.auth import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, username: str, email: str, password: str):
    hashed_password = pwd_context.hash(password)
    new_user = User(username=username, email=email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not pwd_context.verify(password, user.password_hash):
        return False
    return user

def login_user(db: Session, username: str, password: str):
    user = authenticate_user(db, username, password)
    if not user:
        return None
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
