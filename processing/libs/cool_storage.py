from google.cloud import storage
from .settings import traer_configuraciones

from functools import lru_cache
class CoolStorage:

    def __init__(self):
        settings = traer_configuraciones()

        self.credentials = settings.CREDENTIAL_FILE_STORAGE
        self.bucket = settings.BUCKET_NAME
        self.storage_client = storage.Client.from_service_account_json(self.credentials)

    def upload_file(self, video_id: int, nombre_archivo: str):
        print(f"Uploading file {nombre_archivo} to bucket {video_id}")

        bucket = self.storage_client.get_bucket(self.bucket)

        file_path = f"videos/{video_id}/{nombre_archivo}"

        blob = bucket.blob(file_path)
        blob.upload_from_filename(nombre_archivo, content_type='video/mp4')

        return f'gs://idrl_bucket/{file_path}'
    
    def download_file(self, video_id: int, file_name: str):
        bucket = self.storage_client.get_bucket(self.bucket)
        blob = bucket.blob(f"videos/{video_id}/original_{file_name}")
        blob.download_to_filename(f"{file_name}")
    
@lru_cache
def crear_instancia_de_cloud_storage():
    return CoolStorage()