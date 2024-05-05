from fastapi import APIRouter, status, UploadFile, File, Depends
from fastapi.responses import FileResponse
from dtos import TareaDto, TareaResponse
from servicios import save_video, descargar_video_procesado
from jwt_manager import JWTBearer
import os

router = APIRouter()

#Endpoint para carga un video e iniciar la tarea de procesamiento
@router.post("/api/tasks", status_code=status.HTTP_201_CREATED, dependencies=[Depends(JWTBearer())])
async def upload_video(video: UploadFile = File(...)) -> str:
    video_response = await save_video(video)
    return f"Tarea de edición de video creada exitosamente, id: {video_response.id}"
    
#Endpoint para descargar el video procesado
@router.get("/api/tasks/{tarea_id}/download", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def descargar_video_procesado(tarea_id: int):
    ruta_video_procesado = None 
    try: 
        ruta_video_procesado = descargar_video_procesado()
    except Exception as e:
        return {"error": "Descargando el video"}
    
    if not ruta_video_procesado:
        return {"error": "Video procesado no encontrado"}

    # Devolver el archivo como respuesta utilizando FileResponse
    return FileResponse(ruta_video_procesado, media_type="video/mp4", filename="video_procesado.mp4")

