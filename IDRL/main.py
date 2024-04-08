from typing import Union
from fastapi import FastAPI, status

from dtos import PilotoDto, PilotoResponse
from servicios import crear_piloto_svc, traer_pilotos_svc
from rutas import piloto_ruta

app = FastAPI()
app.include_router(piloto_ruta.router)





    