from pydantic import BaseModel
from typing import Optional

class PilotoDto(BaseModel):
    usuario: str
    email: str
    pais: str
    contrasena: str

class PilotoResponse(BaseModel):
    mensaje: Optional[str]

    class Config:
        orm_mode = True
