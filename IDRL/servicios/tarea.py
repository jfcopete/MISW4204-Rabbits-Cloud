from modelos import Piloto, Tarea
from sqlmodel import Session
from libs.database import engine
from dtos import TareaResponse
from libs.settings import traer_configuraciones
from libs.cold_storage import crear_instancia_de_cloud_storage
import os

# Servicio para traer todas las tareas de un piloto
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

# Servicio para traer una tarea por id
def traer_tarea_por_id(tarea_id: int) -> dict:
    settings = traer_configuraciones()

    with Session(engine) as session:
        tarea = session.query(Tarea).filter(Tarea.id == tarea_id).first()
        if not tarea:   
            return {"error": "Tarea no encontrada"}
        download_link = f"{settings.SERVER_IP}/api/tasks/{tarea_id}/download"

        tarea_response = {
        "id": tarea.id,
        "estado": tarea.estado,
        "url": tarea.url,
        "download_link": download_link,
        "nombre_archivo": tarea.nombre_archivo,
        }

        return tarea_response   
    
# Servicio para crear una nueva tarea
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

# Servicio para actualizar una tarea
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

# Servicio para borrar una tarea
def borrar_tarea_por_id(tarea_id: int) -> dict:
    with Session(engine) as session:
        tarea = session.query(Tarea).filter(Tarea.id == tarea_id).first()

        if not tarea:
            return {
                "error": "Tarea no encontrada"
            }
        
        if tarea.estado.value != "processed":
            return {
                "error": "Tarea no ha sido procesada"
            }
        
        try:
            cold_storage = crear_instancia_de_cloud_storage()
            cold_storage.delete_file(tarea_id, f'original_{tarea.nombre_archivo}')
            cold_storage.delete_file(tarea_id, f'editado_{tarea.nombre_archivo}')
        except Exception as e:
            return {
                "error": "Error al borrar el archivo"
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

def actualizar_tarea_url(tarea_id: str, tarea_url: str) -> TareaResponse:
     with Session(engine) as session:
        tarea = session.get(Tarea, tarea_id)
        if not tarea:
            return {
                "error": "Tarea no encontrada"
            }
        tarea.url = tarea_url,
        session.commit()
        return {
            "id": tarea.id,
            "nombre_archivo": tarea.nombre_archivo,
            "url": tarea_url,
            "estado": tarea.estado,
            "numero_votos": tarea.numero_votos,
            "marca_de_carga": tarea.marca_de_carga,
            "piloto_id": tarea.piloto_id
        }