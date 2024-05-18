from google.cloud import storage
from fastapi import HTTPException
from functools import lru_cache
import os
import json
class ColdStorage:

    def __init__(self):
            self.credentials = os.environ.get("CREDENTIAL_FILE_STORAGE")
            self.bucket = os.environ.get("BUCKET_NAME")
            credentials_dict = json.loads(self.credentials)
            self.storage_client = storage.Client.from_service_account_info(credentials_dict)

    def upload_file(self, video_id: int, archivo: str):
        try:
            ruta_origen = os.path.abspath(archivo)
            if not os.path.isfile(ruta_origen):
                return None
            bucket = self.storage_client.get_bucket(self.bucket)
            ruta_destino = f"videos/{video_id}/{archivo}"
            blob = bucket.blob(ruta_destino)
            with open(ruta_origen, 'rb') as file:
                blob.upload_from_file(file, content_type='video/mp4')
            return f'{ruta_destino}'
        except Exception as e:
            print("Error al subir el archivo:", str(e))
            return None
    
    def download_file(self, video_id: int, file_name: str = 'pepe.mp4'):
        bucket = self.storage_client.get_bucket(self.bucket)
        blob = bucket.blob(f'videos/{video_id}/original_{file_name}')        
        if not blob.exists():
            raise HTTPException(status_code=404, detail="Archivo no encontrado")
        blob.download_to_filename(f"{file_name}")

    def delete_file(self, video_id: int, file_name: str):
        bucket = self.storage_client.get_bucket(self.bucket)
        blob = bucket.blob(f'videos/{video_id}/{file_name}')
        if not blob.exists():
            raise HTTPException(status_code=404, detail="Archivo no encontrado")
        return blob.delete()
    
@lru_cache
def crear_instancia_de_cloud_storage():
    return ColdStorage()