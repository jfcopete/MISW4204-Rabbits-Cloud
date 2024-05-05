from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    BUCKET_NAME: str
    CREDENTIAL_FILE: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int

    model_config = SettingsConfigDict(env_file=".env")

    
@lru_cache
def traer_configuraciones():
    return Settings()

