from dtos import PilotoDto, PilotoResponse
from dtos.authentication import SignUpRequest, User
from modelos import Piloto
from sqlmodel import Session
from jwt_manager import create_token
from libs.database import engine
import re

# Servicio para traer todos los pilotos
def traer_pilotos_svc():
    with Session(engine) as session:
        pilotos = session.query(Piloto).all()
        return pilotos

# Servicio para crear un piloto
def crear_piloto_svc(request: SignUpRequest) -> PilotoResponse:
    # Verificar si las contraseñas coinciden
    if request.password1 != request.password2:
        return PilotoResponse(mensaje="Las contraseñas no coinciden")
    
    # Verificar longitud mínima de la contraseña
    if len(request.password1) < 8:
        return PilotoResponse(mensaje="La contraseña debe tener al menos 8 caracteres")
    
    # Verificar al menos una mayúscula
    if not re.search(r"[A-Z]", request.password1):
        return PilotoResponse(mensaje="La contraseña debe tener al menos una mayúscula")
    
    # Verificar al menos una minúscula
    if not re.search(r"[a-z]", request.password1):
        return PilotoResponse(mensaje="La contraseña debe tener al menos una minúscula")
    
    # Verificar al menos un carácter especial
    if not re.search(r"[!@#$%^&*()_+{}|:<>?~-]", request.password1):
        return PilotoResponse(mensaje="La contraseña debe tener al menos un carácter especial")
    
    # Verificar si el usuario ya existe
    with Session(engine) as session:
        existing_piloto = session.query(Piloto).filter(Piloto.usuario == request.username).first()
        if existing_piloto:
            return PilotoResponse(mensaje="El usuario ya existe")
        
        # Verificar si el correo electrónico ya existe
        existing_email = session.query(Piloto).filter(Piloto.email == request.email).first()
        if existing_email:
            return PilotoResponse(mensaje="El correo electrónico ya está en uso")
        
        # Crear el nuevo piloto
        nuevo_piloto = Piloto(
            usuario=request.username,
            email=request.email,
            contrasena=request.password1,
            pais=request.pais
        )
        session.add(nuevo_piloto)
        session.commit()
        
        # Creación exitosa de usuario
        return PilotoResponse(
            mensaje="Cuenta creada exitosamente"
        )

# Servicio para autenticar un piloto
def autenticar_piloto_svc(request: User) -> str:
    with Session(engine) as session:
        piloto = session.query(Piloto).filter(Piloto.usuario == request.username).first() 
        if not piloto:
            return {"mensaje" : "Usuario no existe"}
        if not piloto.contrasena == request.password:
            return {"mensaje" : "Password incorrecta"}
        created_token : str = create_token(request.dict())
        return {"token" : created_token}
