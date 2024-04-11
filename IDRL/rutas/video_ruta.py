from fastapi import APIRouter, status, UploadFile, File
from dtos import VideoDto, VideoResponse
from servicios import save_video

router = APIRouter()

@router.post("/video", status_code=status.HTTP_201_CREATED)
def upload_video(video: UploadFile = File(...)) -> VideoResponse:
    video_response = save_video(video)
    return {
        "id": video_response.id,
        "estado": video_response.estado,
        "url": video_response.url
    }