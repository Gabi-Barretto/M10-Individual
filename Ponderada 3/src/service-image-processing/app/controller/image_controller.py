from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.image_service import remove_background

router = APIRouter()

@router.post("/remove-background")
async def remove_background_endpoint(file: UploadFile = File(...)):
    try:
        result = await remove_background(file)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
