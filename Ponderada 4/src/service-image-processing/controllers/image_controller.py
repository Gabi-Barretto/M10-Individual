from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from services.image_service import remove_background
import requests
import base64

LOG_ENDPOINT = "http://localhost:8000/log/logs"

def log_usage(level: str, message: str):
    try:
        response = requests.post(LOG_ENDPOINT, json={"level": level, "message": message})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to log usage: {e}")

router = APIRouter()

@router.post("/remove-background")
async def remove_background_endpoint(file: UploadFile = File(...)):
    try:
        log_usage(level="INFO", message="Received request to remove background")
        result = await remove_background(file)
        base64_image = base64.b64encode(result).decode('utf-8')
        log_usage(level="INFO", message="Image successfully encoded to base64")
        return JSONResponse(content={"base64_image": base64_image})
    except Exception as e:
        log_usage(level="ERROR", message=f"Error in endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error in endpoint: {str(e)}")
