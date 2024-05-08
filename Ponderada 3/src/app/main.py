from fastapi import FastAPI, HTTPException, Depends, Request, Form, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from rabbitmq.producer import log_to_rabbit as send_log_message

from sqlalchemy.orm import Session
from jose import jwt, JWTError

from database.database import SessionLocal, engine, create_db
from database.models import User, Base

import uvicorn
import sys
import pika

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency for database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/user-login", response_class=HTMLResponse)
def user_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/user-register", response_class=HTMLResponse)
def user_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
def register_user(request: Request, user_data: dict = Body(...), db: Session = Depends(get_db)):
    name = user_data['name']
    email = user_data['email']
    password = user_data['password']
    user = User(name=name, email=email, password=password)
    db.add(user)
    db.commit()
    send_log_message(f"New user registered: {email}")
    return {"message": "User registered successfully!"}

@app.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email, User.password == password).first()
    if not user:
        return templates.TemplateResponse("error.html", {"request": request, "message": "Bad username or password"})
    access_token = jwt.encode({"sub": user.id}, "goku-vs-vegeta", algorithm="HS256")
    response = templates.TemplateResponse("content.html", {"request": request, "message": "Login Successful"})
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    send_log_message(f"User logged in: {email}")
    return response

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [user.serialize() for user in users]

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.serialize()

@app.put("/users/{user_id}")
def update_user(user_id: int, name: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = name
    user.email = email
    user.password = password
    db.commit()
    return user.serialize()

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}

if len(sys.argv) > 1 and sys.argv[1] == 'create_db':
    create_db()
    print("Database created successfully")
    sys.exit(0)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
