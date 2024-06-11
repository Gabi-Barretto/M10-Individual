from fastapi import APIRouter
from app.controllers import image_controller

router = APIRouter()

router.include_router(image_controller.router, prefix="/image", tags=["image"])
