from modelos import Piloto, Tarea
from sqlmodel import Session
from libs.database import engine
from dtos import TareaResponse
import os

def traer_tareas_por_piloto(piloto_id: int, max: int, orden: int) -> list[TareaResponse]:
    with Session(engine) as session:
        # Construir la consulta base filtrando por piloto_id
        query = session.query(Tarea).filter(Tarea.piloto_id == piloto_id)
        
        # Aplicar orden ascendente o descendente según el parámetro 'orden'
        if orden == 0:
            query = query.order_by(Tarea.id.asc())
        elif orden == 1:
            query = query.order_by(Tarea.id.desc())
        
        # Limitar el número máximo de tareas
        query = query.limit(max)
        
        # Ejecutar la consulta y obtener los resultados
        tareas = query.all()
        return tareas

def traer_tarea_por_id(tarea_id: int) -> dict:
    with Session(engine) as session:
        print("buscando tarea")
        tarea = session.get(Tarea, tarea_id)
        if not tarea:   
            return {"error": "Tarea no encontrada"}
        current_path = os.getcwd()
        print("tarea encontrada")
        video_procesado_path = f"{current_path}/videos_procesados/{tarea.id}/procesado.mp4"
        download_link = f"http://localhost:8000{video_procesado_path}"

        tarea_response = {
        "id": tarea.id,
        "estado": tarea.estado,
        "url": tarea.url,
        "download_link": download_link  
        }

        return tarea_response   
    

def crear_tarea(nombre_archivo: str, url: str, piloto_id: str) -> TareaResponse:
    tarea = Tarea(
        nombre_archivo=nombre_archivo,
        piloto_id=piloto_id,
        url=url,
    )

    with Session(engine) as session:
        session.add(tarea)
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
    
def actualizar_tarea(tarea_id: int) -> TareaResponse:
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

def borrar_tarea_por_id(tarea_id: int) -> TareaResponse:
    with Session(engine) as session:
        tarea = session.get(Tarea, tarea_id)
        if not tarea:
            return {
                "error": "Tarea no encontrada"
            }
        tarea.estado = "deleted"
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