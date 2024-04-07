from typing import Union
from fastapi import FastAPI

from dtos import PilotoDto, PilotoResponse
from servicios import crear_piloto_svc

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World 2"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/piloto")
def crear_piloto(piloto: PilotoDto) -> PilotoResponse:
    piloto = crear_piloto_svc(piloto)
    return piloto
    