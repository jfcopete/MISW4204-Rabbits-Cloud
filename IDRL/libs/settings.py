from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    BUCKET_NAME: str
    CREDENTIAL_FILE: str

    model_config = SettingsConfigDict(env_file=".env")

    
@lru_cache
def traer_configuraciones():
    return Settings()

