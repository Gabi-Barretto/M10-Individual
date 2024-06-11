from fastapi import APIRouter
from controllers import log_controller

router = APIRouter()

router.include_router(log_controller.router, prefix="/log", tags=["log"])
