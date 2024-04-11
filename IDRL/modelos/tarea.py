from datetime import datetime as date
from typing import Optional
from enum import Enum

from sqlmodel import Field, SQLModel, Enum as SQLEnum

class ESTADO_VIDEO(str, Enum):
    PROCESSED: str = "processed"
    UPLOADED: str = "uploaded"

class Tarea(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre_archivo: str
    url: str
    estado: ESTADO_VIDEO = Field(default=ESTADO_VIDEO.UPLOADED.value, sa_column=SQLEnum(ESTADO_VIDEO))
    numero_votos: int = Field(default=0)
    marca_de_carga: date = Field(default_factory=date.now)
    piloto_id: int = Field(foreign_key="piloto.id")
    