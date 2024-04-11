from fastapi import UploadFile
from pydantic import BaseModel

class VideoDto(BaseModel):
    usuario: str
    video: UploadFile

class VideoResponse(BaseModel):
    id: int
    estado: str
    url: str