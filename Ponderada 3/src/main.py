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
import pika
import datetime
import os
from dotenv import load_dotenv

# Carrega o arquivo .env
load_dotenv()

class RegisterData(BaseModel):
    name: str
    email: str
    password: str

class Message(BaseModel):
    date: datetime.datetime = None
    msg: str

# Cria uma função que faz o envio das mensagens para o RabbitMQ
def send_message_rabbitmq(msg: Message):
    # Verifica se as variáveis de ambiente estão definidas
    if "RABBITMQ_HOST" not in os.environ or "RABBITMQ_PORT" not in os.environ:
        raise Exception("RABBITMQ_HOST and RABBITMQ_PORT must be defined in environment variables")

    credentials = pika.PlainCredentials(os.environ["RABBITMQ_DEFAULT_USER"], os.environ["RABBITMQ_DEFAULT_PASS"])
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        os.environ["RABBITMQ_HOST"],
        os.environ["RABBITMQ_PORT"],
        '/',
        credentials))
    channel = connection.channel()
    channel.queue_declare(queue=os.environ["RABBITMQ_QUEUE"])
    channel.basic_publish(exchange='', routing_key=os.environ["RABBITMQ_QUEUE"], body=f"{msg.date} - {msg.msg}")
    connection.close()

# Cria uma função que recebe as mensagens para o RabbitMQ
def receive_last_message_rabbitmq():
    # Verifica se as variáveis de ambiente estão definidas
    if "RABBITMQ_HOST" not in os.environ or "RABBITMQ_PORT" not in os.environ:
        raise Exception("RABBITMQ_HOST and RABBITMQ_PORT must be defined in environment variables")

    credentials = pika.PlainCredentials(os.environ["RABBITMQ_DEFAULT_USER"], os.environ["RABBITMQ_DEFAULT_PASS"])
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        os.environ["RABBITMQ_HOST"],
        os.environ["RABBITMQ_PORT"],
        '/',
        credentials))
    channel = connection.channel()
    channel.queue_declare(queue=os.environ["RABBITMQ_QUEUE"])

    method_frame, header_frame, body = channel.basic_get(queue=os.environ["RABBITMQ_QUEUE"], auto_ack=True)
    connection.close()

    if method_frame:
        return body.decode()
    else:
        return "No message returned"

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

    log_message = Message(date=datetime.datetime.now(), msg=f"User {email} registered.")
    send_message_rabbitmq(log_message)

    # Consumir e imprimir o último log enviado
    last_message = receive_last_message_rabbitmq()
    print(f"Last log message: {last_message}")

    # Enviar log para RabbitMQ
    log_message = Message(date=datetime.datetime.now(), msg=f"User {email} registered.")
    send_message_rabbitmq(log_message)

    return JSONResponse(content={"message": "User registered successfully!"})

@app.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email, User.password == password).first()
    if not user:
        return templates.TemplateResponse("error.html", {"request": request, "message": "Bad username or password"})
    access_token = jwt.encode({"sub": user.id}, "goku-vs-vegeta", algorithm="HS256")
    response = templates.TemplateResponse("content.html", {"request": request, "message": "Login Successful"})
    response.set_cookie(key="access_token", value=access_token, httponly=True)

    # Enviar log para RabbitMQ
    log_message = Message(date=datetime.datetime.now(), msg=f"User {email} logged in.")
    send_message_rabbitmq(log_message)
    receive_last_message_rabbitmq()

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

    # Enviar log para RabbitMQ
    log_message = Message(date=datetime.datetime.now(), msg=f"User {email} updated.")
    send_message_rabbitmq(log_message)

    return user.serialize()

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()

    # Enviar log para RabbitMQ
    log_message = Message(date=datetime.datetime.now(), msg=f"User {user.email} deleted.")
    send_message_rabbitmq(log_message)

    return {"message": "User deleted"}

@app.post("/send-log", response_class=JSONResponse)
async def send_log(msg: Message):
    try:
        send_message_rabbitmq(msg)
        return JSONResponse(content={"message": "Log sent successfully!"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/receive-log")
async def receive_log():
    try:
        messages = []
        def callback(ch, method, properties, body):
            messages.append(body.decode())
            ch.basic_ack(delivery_tag=method.delivery_tag)
        
        receive_message_rabbitmq(callback)
        
        return JSONResponse(content={"messages": messages})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if len(sys.argv) > 1 and sys.argv[1] == 'create_db':
    create_db()
    print("Database created successfully")
    sys.exit(0)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
