from fastapi import APIRouter, status, UploadFile, File, Depends, Response
from fastapi.responses import StreamingResponse
from dtos import TareaDto, TareaResponse
from servicios import save_video, descargar_video_procesado
from jwt_manager import JWTBearer

router = APIRouter()

#Endpoint para carga un video e iniciar la tarea de procesamiento
@router.post("/api/tasks", status_code=status.HTTP_201_CREATED, dependencies=[Depends(JWTBearer())])
async def upload_video(video: UploadFile = File(...)) -> str:
    video_response = await save_video(video)
    return f"Tarea de edición de video creada exitosamente, id: {video_response.id}"
    
#Endpoint para descargar el video procesado
@router.get("/api/tasks/{tarea_id}/download", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def descargar_video(tarea_id: int):
    contenido_archivo = None 
    try: 
        contenido_archivo = descargar_video_procesado(tarea_id)
    except Exception as e:
        return {"error": "No fue posible descargar el video"}
    
    if not contenido_archivo:
        return {"error": "Video procesado no encontrado"}
    
    return StreamingResponse(
        content=contenido_archivo, 
        media_type="video/mp4", 
        headers={"Content-Disposition": "attachment; filename=video_procesado.mp4"}
    )

