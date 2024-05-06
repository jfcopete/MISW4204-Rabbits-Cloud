from typing import Optional

from sqlmodel import Field, SQLModel

class Piloto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario: str
    email: str
    pais: str
    contrasena: str
    