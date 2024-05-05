from fastapi import FastAPI
from libs.cool_storage import crear_instancia_de_cloud_storage
from libs.settings import traer_configuraciones
from kafka_consumer import router


app = FastAPI()

traer_configuraciones()
crear_instancia_de_cloud_storage()

app.include_router(router)

