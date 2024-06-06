from fastapi import APIRouter, HTTPException
from schemas.user_schema import ImageRequest
from services.image_service import remove_background_from_base64

router = APIRouter()

@router.post("/remove-bg", tags=["Image"], status_code=200)
async def remove_bg(image_request: ImageRequest):
    try:
        base64_result = remove_background_from_base64(image_request.base64_image)
        return {"base64_image": base64_result}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
