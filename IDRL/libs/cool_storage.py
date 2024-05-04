from google.cloud import storage
from libs import traer_configuraciones

from functools import lru_cache
class CoolStorage:

    def __init__(self):
        settings = traer_configuraciones()

        self.credentials = settings.CREDENTIAL_FILE
        self.bucket = settings.BUCKET_NAME
        self.storage_client = storage.Client.from_service_account_json(self.credentials)

    def upload_file(self, video_id: int, archivo):

        bucket = self.storage_client.get_bucket(self.bucket)

        file_path = f"videos/{video_id}/original_{archivo.filename}"

        blob = bucket.blob(file_path)
        blob.upload_from_file(archivo.file, content_type='video/mp4')

        return f'gs://{file_path}'
    
@lru_cache
def crear_instancia_de_cloud_storage():
    return CoolStorage()