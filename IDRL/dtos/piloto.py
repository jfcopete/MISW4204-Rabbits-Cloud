from pydantic import BaseModel

class PilotoDto(BaseModel):
    usuario: str
    email: str
    pais: str
    contrasena: str

class PilotoResponse(BaseModel):
    id: int
    usuario: str
    email: str
    pais: str