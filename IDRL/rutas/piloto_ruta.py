from fastapi import APIRouter, status, Depends
from dtos.authentication import SignUpRequest, User
from dtos import PilotoResponse, PilotoDto
from servicios.tarea import traer_tareas_por_piloto
from servicios import crear_piloto_svc, traer_pilotos_svc, autenticar_piloto_svc
from jwt_manager import JWTBearer

router = APIRouter()

@router.get("/pilotos", status_code=status.HTTP_200_OK)
def traer_pilotos():
    pilotos = traer_pilotos_svc()
    return pilotos    

@router.post("/api/auth/signup", status_code=status.HTTP_201_CREATED, response_model=PilotoResponse)
def signup_piloto(request: SignUpRequest) -> PilotoResponse:
    piloto_respuesta = crear_piloto_svc(request)
    return piloto_respuesta

@router.post("/api/auth/login", status_code=status.HTTP_200_OK)
def login(user: User):
    user = autenticar_piloto_svc(user)
    return user

@router.get("/api/tasks", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())] )
def traer_tareas(piloto_id: int, max: int=10, orden: int=0):
    tareas = traer_tareas_por_piloto(piloto_id, max, orden)
    return tareas