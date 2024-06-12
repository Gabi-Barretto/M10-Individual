from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from services.image_service import remove_background
import io

router = APIRouter()

@router.post("/remove-background")
async def remove_background_endpoint(file: UploadFile = File(...)):
    try:
        result = await remove_background(file)
        base64_image = base64.b64encode(result).decode('utf-8')
        return JSONResponse(content={"base64_image": base64_image})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
