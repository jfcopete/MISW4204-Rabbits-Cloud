from fastapi import APIRouter, status, UploadFile, File, Depends
from dtos import TareaDto, TareaResponse
from servicios import save_video
from jwt_manager import JWTBearer

router = APIRouter()

@router.post("/api/tasks", status_code=status.HTTP_201_CREATED, dependencies=[Depends(JWTBearer())])
async def upload_video(video: UploadFile = File(...)) -> str:
    video_response = await save_video(video)
    return f"Tarea de edición de video creada exitosamente, id: {video_response.id}"
    