from datetime import datetime as date
from typing import Optional
from enum import Enum

from sqlmodel import Field, SQLModel, Enum as SQLEnum

class ESTADO_VIDEO(str, Enum):
    PROCESSED: str = "processed"
    PENDING: str = "uploaded"

class Video(SQLModel, table=True):    
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    url: str
    es_valido: bool
    estado: ESTADO_VIDEO = Field(sa_column=SQLEnum(ESTADO_VIDEO))
    numero_votos: int    
    # fecha_creacion: Field(default=date.now())
