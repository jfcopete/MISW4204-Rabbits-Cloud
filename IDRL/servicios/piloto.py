from dtos import PilotoDto
from modelos import Piloto
from sqlmodel import Session
from libs.database import engine

def traer_pilotos_svc():
    with Session(engine) as session:
        pilotos = session.query(Piloto).all()
        return pilotos

def crear_piloto_svc(nuevo_piloto: PilotoDto):
    piloto = Piloto(
        usuario=nuevo_piloto.usuario,
        email=nuevo_piloto.email,
        pais=nuevo_piloto.pais,
        contrasena=nuevo_piloto.contrasena
    )

    with Session(engine) as session:
        session.add(piloto)
        session.commit()
        return {
            "id": piloto.id,
            "usuario": piloto.usuario,
            "email": piloto.email,
            "pais": piloto.pais
        }

