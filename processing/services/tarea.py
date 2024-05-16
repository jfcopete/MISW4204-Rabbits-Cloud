from sqlmodel import Session
from libs.database import engine
from libs.settings import traer_configuraciones
from modelos import Tarea


# Servicio para traer una tarea por id
def traer_tarea_por_id(tarea_id: int) -> dict:
    settings = traer_configuraciones()
    with Session(engine) as session:
        tarea = session.get(Tarea, tarea_id)
        if not tarea:   
            return {"error": "Tarea no encontrada"}
        download_link = f"http://{settings.SERVER_IP}/api/tasks/{tarea_id}/download"

        tarea_response = {
        "id": tarea.id,
        "estado": tarea.estado,
        "url": tarea.url,
        "download_link": download_link,
        "nombre_archivo": tarea.nombre_archivo,
        }

        return tarea_response 
    
# Servicio para actualizar una tarea
def actualizar_tarea(tarea_id: int):
    with Session(engine) as session:
        tarea = session.get(Tarea, tarea_id)
        if not tarea:
            return {
                "error": "Tarea no encontrada"
            }
        tarea.estado = "processed"
        session.commit()
        return {
            "id": tarea.id,
            "nombre_archivo": tarea.nombre_archivo,
            "url": tarea.url,
            "estado": tarea.estado,
            "numero_votos": tarea.numero_votos,
            "marca_de_carga": tarea.marca_de_carga,
            "piloto_id": tarea.piloto_id
        }