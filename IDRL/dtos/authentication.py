from pydantic import BaseModel

class SignUpRequest(BaseModel):
    username: str
    email: str
    password1: str
    password2: str
    pais: str

class User(BaseModel):
    username: str
    password: str