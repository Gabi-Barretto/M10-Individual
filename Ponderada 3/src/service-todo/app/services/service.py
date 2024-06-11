from sqlalchemy.orm import Session
from models.todo_model import TodoItem

def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TodoItem).offset(skip).limit(limit).all()

def create_todo_item(db: Session, title: str, description: str = None):
    todo_item = TodoItem(title=title, description=description)
    db.add(todo_item)
    db.commit()
    db.refresh(todo_item)
    return todo_item

def get_todo_item(db: Session, todo_id: int):
    return db.query(TodoItem).filter(TodoItem.id == todo_id).first()

def update_todo_item(db: Session, todo_id: int, title: str = None, description: str = None, completed: bool = None):
    todo_item = get_todo_item(db, todo_id)
    if todo_item:
        if title:
            todo_item.title = title
        if description:
            todo_item.description = description
        if completed is not None:
            todo_item.completed = completed
        db.commit()
        db.refresh(todo_item)
    return todo_item

def delete_todo_item(db: Session, todo_id: int):
    todo_item = get_todo_item(db, todo_id)
    if todo_item:
        db.delete(todo_item)
        db.commit()
    return todo_item
