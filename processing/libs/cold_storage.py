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
        bucket = self.storage_client.get_bucket(self.bucket)
        file_path = f"videos/{video_id}/{archivo}"
        blob = bucket.blob(file_path)
        blob.upload_from_file(archivo, content_type='video/mp4')
        return f'{file_path}'
    
    def download_file(self, video_id: int, file_name: str = 'pepe.mp4'):
        print("download file", video_id, file_name)
        bucket = self.storage_client.get_bucket(self.bucket)
        print("bucket: ", bucket)
        blob = bucket.blob(f'videos/{video_id}/original_{file_name}')        
        if not blob.exists():
            raise HTTPException(status_code=404, detail="Archivo no encontrado")
        print("blob exists")
        #bytes_buffer = blob.download_as_bytes()
        blob.download_to_filename(f"{file_name}")
        #return bytes_buffer

    def delete_file(self, video_id: int, file_name: str):
        bucket = self.storage_client.get_bucket(self.bucket)
        blob = bucket.blob(f'videos/{video_id}/{file_name}')
        if not blob.exists():
            raise HTTPException(status_code=404, detail="Archivo no encontrado")
        return blob.delete()
    
@lru_cache
def crear_instancia_de_cloud_storage():
    return ColdStorage()