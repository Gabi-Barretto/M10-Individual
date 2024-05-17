from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.database import SessionLocal, create_db
from database.models import User

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

if len(sys.argv) > 1 and sys.argv[1] == 'create_db':
    create_db()
    print("Database created successfully")
    sys.exit(0)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/novo", response_class=HTMLResponse)
async def register_pedido(request: Request, db: Session = Depends(get_db)):
    try:
        # Tentando ler JSON primeiro
        data = await request.json()
    except:
        # Se falhar, tente ler como dados de formulário
        form_data = await request.form()
        data = { "name": form_data.get("name"), "email": form_data.get("email"), "pedido": form_data.get("pedido") }
    
    # Verifica se algum dos campos está vazio
    if not all(data.values()):
        return JSONResponse(status_code=400, content={"message": "Missing data"})

    name = data["name"]
    email = data["email"]
    pedido = data["pedido"]

    # Logica de criacao de usuario
    user = User(name=name, email=email, pedido=pedido)
    db.add(user)
    db.commit()

    return JSONResponse(content={"message": "Nova nota adicionada successfully!"})

@app.get("/pedidos", response_class=HTMLResponse)
def get_pedidos(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return JSONResponse(content=[user.serialize() for user in users])

@app.get("/pedidos/{pedido_id}", response_class=HTMLResponse)
def get_user(pedido_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == pedido_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return JSONResponse(content=user.serialize())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
