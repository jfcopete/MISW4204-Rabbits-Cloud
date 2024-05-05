from fastapi import FastAPI
from .cool_storage import crear_instancia_de_cloud_storage
from .settings import traer_configuraciones


app = FastAPI()

traer_configuraciones()
crear_instancia_de_cloud_storage()

