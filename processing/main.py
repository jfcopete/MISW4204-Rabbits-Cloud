from fastapi import FastAPI
from libs.cold_storage import crear_instancia_de_cloud_storage
from libs.settings import traer_configuraciones
from cloud_pubsub_consumer import router as pubsub_router


app = FastAPI()

traer_configuraciones()
crear_instancia_de_cloud_storage()

app.include_router(pubsub_router)

