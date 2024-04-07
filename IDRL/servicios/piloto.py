from dtos import PilotoDto
from modelos import Piloto
from sqlmodel import Session
from libs.database import engine


def crear_piloto_svc(nuevo_piloto: PilotoDto):
    piloto = Piloto(
        usuario=nuevo_piloto.usuario,
        email=nuevo_piloto.email,
        pais=nuevo_piloto.pais,
        contrasena=nuevo_piloto.contrasena
    )

    with Session(engine) as session:
        session.add(piloto)
        res = session.commit()
        print(res)
        return res

