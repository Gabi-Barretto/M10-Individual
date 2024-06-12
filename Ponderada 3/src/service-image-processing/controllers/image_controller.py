from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from services.image_service import remove_background
import io

router = APIRouter()

@router.post("/remove-background")
async def remove_background_endpoint(file: UploadFile = File(...)):
    try:
        result = await remove_background(file)
        return StreamingResponse(io.BytesIO(result), media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
