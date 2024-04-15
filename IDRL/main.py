from typing import Union
from fastapi import FastAPI, status

from dtos import PilotoDto, PilotoResponse
from servicios import crear_piloto_svc, traer_pilotos_svc
from rutas import piloto_ruta, video_ruta, kafka_producer, kafka_consumer

app = FastAPI()
app.include_router(piloto_ruta.router)
app.include_router(video_ruta.router)
app.include_router(kafka_producer.router)
app.include_router(kafka_consumer.router)

