import os
from fastapi import FastAPI
from libs.cold_storage import crear_instancia_de_cloud_storage
from libs.settings import traer_configuraciones
from rutas import piloto_ruta, video_ruta
from libs.secret_manager import access_secret_version


app = FastAPI()

# Acceder a los secretos y configurarlos como variables de entorno
os.environ['CREDENTIAL_FILE_STORAGE'] = access_secret_version("CREDENTIAL_FILE_STORAGE")
os.environ['CREDENTIAL_FILE_PUBSUB'] = access_secret_version("CREDENTIAL_FILE_PUBSUB")

# Crear archivos temporales para las credenciales si es necesario
with open('/tmp/storage_credentials.json', 'w') as f:
    f.write(os.environ['CREDENTIAL_FILE_STORAGE'])

with open('/tmp/pubsub_credentials.json', 'w') as f:
    f.write(os.environ['CREDENTIAL_FILE_PUBSUB'])

# Configurar las variables de entorno para que apunten a los archivos temporales
os.environ['GOOGLE_APPLICATION_CREDENTIALS_STORAGE'] = '/tmp/storage_credentials.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS_PUBSUB'] = '/tmp/pubsub_credentials.json'


traer_configuraciones()
crear_instancia_de_cloud_storage()

app.include_router(piloto_ruta.router)
app.include_router(video_ruta.router)


