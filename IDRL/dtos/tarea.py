from fastapi import UploadFile
from pydantic import BaseModel

class TareaDto(BaseModel):
    usuario: str
    video: UploadFile

class TareaResponse(BaseModel):
    id: int
    estado: str
    url: str