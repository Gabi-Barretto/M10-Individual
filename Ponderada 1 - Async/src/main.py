from fastapi import FastAPI, HTTPException, Depends, Request, Form, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from database.database import SessionLocal, engine, create_db
from database.models import User, Base

import uvicorn
import sys

class LoginData(BaseModel):
    email: str
    password: str

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

@app.post("/register", response_class=JSONResponse)
async def register_user(request: Request, db: Session = Depends(get_db)):
    try:
        # Tentando ler JSON primeiro
        data = await request.json()
    except:
        # Se falhar, tente ler como dados de formulário
        form_data = await request.form()
        data = { "name": form_data.get("name"), "email": form_data.get("email"), "password": form_data.get("password") }
    
    # Verifica se algum dos campos está vazio
    if not all(data.values()):
        return JSONResponse(status_code=400, content={"message": "Missing data"})

    name = data["name"]
    email = data["email"]
    password = data["password"]

    # Logica de criacao de usuario
    user = User(name=name, email=email, password=password)
    db.add(user)
    db.commit()
    return JSONResponse(content={"message": "User registered successfully!"})


@app.post("/login", response_class=JSONResponse)
async def login(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
    except:
        form_data = await request.form()
        data = { "email": form_data.get("email"), "password": form_data.get("password") }

    user = db.query(User).filter(User.email == data["email"], User.password == data["password"]).first()
    if not user:
        return JSONResponse(status_code=400, content={"message": "Bad username or password"})
    else:
        access_token = jwt.encode({"sub": user.id}, "goku-vs-vegeta", algorithm="HS256")
        return JSONResponse(status_code=200, content={"message": "Login Successful", "access_token": access_token})
    
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
