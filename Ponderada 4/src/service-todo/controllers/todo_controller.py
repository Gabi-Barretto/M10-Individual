from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from services.todo_service import get_todos, create_todo_item, get_todo_item, update_todo_item, delete_todo_item
from database import get_db
import requests

LOG_ENDPOINT = "http://localhost:8000/log/logs"

def log_usage(level: str, message: str):
    try:
        response = requests.post(LOG_ENDPOINT, json={"level": level, "message": message})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to log usage: {e}")

router = APIRouter()

class TodoCreate(BaseModel):
    title: str
    description: str
    class Config:
        orm_mode = True

class TodoUpdate(BaseModel):
    title: str = None
    description: str = None
    completed: bool = None

@router.get("/todos")
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    log_usage(level="INFO", message="Fetching todos")
    todos = get_todos(db, skip=skip, limit=limit)
    log_usage(level="INFO", message=f"Fetched {len(todos)} todos")
    return todos

@router.post("/todos", response_model=TodoCreate)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    log_usage(level="INFO", message=f"Creating todo item: {todo.title}")
    created_todo = create_todo_item(db=db, title=todo.title, description=todo.description)
    log_usage(level="INFO", message=f"Created todo item with ID: {created_todo.id}")
    return created_todo

@router.get("/todos/{todo_id}")
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    log_usage(level="INFO", message=f"Fetching todo item with ID: {todo_id}")
    db_todo = get_todo_item(db, todo_id=todo_id)
    if db_todo is None:
        log_usage(level="WARN", message=f"Todo item with ID: {todo_id} not found")
        raise HTTPException(status_code=404, detail="Todo not found")
    log_usage(level="INFO", message=f"Fetched todo item with ID: {todo_id}")
    return db_todo

@router.put("/todos/{todo_id}", response_model=TodoUpdate)
def update_todo(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    log_usage(level="INFO", message=f"Updating todo item with ID: {todo_id}")
    updated_todo = update_todo_item(db=db, todo_id=todo_id, title=todo.title, description=todo.description, completed=todo.completed)
    log_usage(level="INFO", message=f"Updated todo item with ID: {todo_id}")
    return updated_todo

@router.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    log_usage(level="INFO", message=f"Deleting todo item with ID: {todo_id}")
    db_todo = delete_todo_item(db, todo_id=todo_id)
    if db_todo is None:
        log_usage(level="WARN", message=f"Todo item with ID: {todo_id} not found")
        raise HTTPException(status_code=404, detail="Todo not found")
    log_usage(level="INFO", message=f"Deleted todo item with ID: {todo_id}")
    return {"message": "Todo deleted"}
