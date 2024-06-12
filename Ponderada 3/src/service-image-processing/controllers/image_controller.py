from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from services.image_service import remove_background
import io
import logging
import base64

logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.post("/remove-background")
async def remove_background_endpoint(file: UploadFile = File(...)):
    try:
        result = await remove_background(file)
        base64_image = base64.b64encode(result).decode('utf-8')
        logging.info("Image successfully encoded to base64.")
        return JSONResponse(content={"base64_image": base64_image})
    except Exception as e:
        logging.error(f"Error in endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error in endpoint: {str(e)}")