from fastapi import APIRouter
from controllers import todo_controller

router = APIRouter()

router.include_router(todo_controller.router, prefix="/todo", tags=["todo"])
