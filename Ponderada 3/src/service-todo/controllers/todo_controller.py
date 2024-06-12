from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from services.todo_service import get_todos, create_todo_item, get_todo_item, update_todo_item, delete_todo_item
from database import get_db
import logging

logging.basicConfig(level=logging.INFO)

router = APIRouter()

class TodoCreate(BaseModel):
    title: str
    description: str

class TodoUpdate(BaseModel):
    title: str = None
    description: str = None
    completed: bool = None

@router.get("/todos")
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos = get_todos(db, skip=skip, limit=limit)
    return todos

@router.post("/todos", response_model=TodoCreate)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    logging.info(f"Received todo: {todo.title}")
    return create_todo_item(db=db, title=todo.title, description=todo.description)

@router.get("/todos/{todo_id}")
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = get_todo_item(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.put("/todos/{todo_id}", response_model=TodoUpdate)
def update_todo(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    return update_todo_item(db=db, todo_id=todo_id, title=todo.title, description=todo.description, completed=todo.completed)

@router.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = delete_todo_item(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted"}
