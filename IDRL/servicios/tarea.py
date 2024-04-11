from modelos import Piloto, Tarea
from sqlmodel import Session
from libs.database import engine
from dtos import TareaResponse

def traer_tareas_por_piloto(piloto_id: int, max: int, orden: int) -> list[TareaResponse]:
    with Session(engine) as session:
        sentencia_sql = session.select(Tarea).where(Tarea.piloto_id == piloto_id).limit(max).order_by(Tarea.id.desc() if orden == 1 else Tarea.id.asc())
        tareas = session.exec(sentencia_sql)
        return tareas

def traer_tarea():
    pass


def crear_tarea(nombre_archivo: str, file_path: str, piloto_id: str) -> TareaResponse:
    tarea = Tarea(
        nombre_archivo=nombre_archivo,
        piloto_id=piloto_id,
        url=file_path,
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