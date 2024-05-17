import os
from fastapi import FastAPI
from libs.cold_storage import crear_instancia_de_cloud_storage
from libs.settings import traer_configuraciones
from rutas import piloto_ruta, video_ruta

app = FastAPI()

traer_configuraciones()
crear_instancia_de_cloud_storage()

app.include_router(piloto_ruta.router)
app.include_router(video_ruta.router)


