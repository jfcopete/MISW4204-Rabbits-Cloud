from fastapi import APIRouter, status, UploadFile, File, Depends
from dtos import TareaDto, TareaResponse
from servicios import save_video
from jwt_manager import JWTBearer

router = APIRouter()

@router.post("/video", status_code=status.HTTP_201_CREATED, dependencies=[Depends(JWTBearer())])
async def upload_video(video: UploadFile = File(...)) -> TareaResponse:
    video_response = await save_video(video)
    return {
        "id": video_response.id,
        "estado": video_response.estado,
        "url": video_response.url
    }