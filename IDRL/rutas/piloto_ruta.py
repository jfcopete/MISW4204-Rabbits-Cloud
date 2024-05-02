from fastapi import APIRouter, status, Depends
from dtos.authentication import SignUpRequest, User
from dtos import PilotoResponse, PilotoDto, TareaResponse
from servicios.tarea import traer_tareas_por_piloto, traer_tarea_por_id, borrar_tarea_por_id
from servicios import crear_piloto_svc, traer_pilotos_svc, autenticar_piloto_svc
from jwt_manager import JWTBearer

router = APIRouter()

#Endpoint para traer todos los pilotos
@router.get("/pilotos", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def traer_pilotos():
    pilotos = traer_pilotos_svc()
    return pilotos    

#Endpoint para crear un piloto
@router.post("/api/auth/signup", status_code=status.HTTP_201_CREATED, response_model=PilotoResponse)
def signup_piloto(request: SignUpRequest) -> PilotoResponse:
    piloto_respuesta = crear_piloto_svc(request)
    return piloto_respuesta

#Endpoint para autenticar un piloto
@router.post("/api/auth/login", status_code=status.HTTP_200_OK)
def login(user: User):
    user = autenticar_piloto_svc(user)
    return user

#Endpoint para traer todas las tareas de un piloto
@router.get("/api/tasks", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())] )
def traer_tareas(piloto_id: int, max: int=10, orden: int=0):
    tareas = traer_tareas_por_piloto(piloto_id, max, orden)
    return tareas

#Endpoint para traer una tarea por id
@router.get("/api/tasks/{id_task}", status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
def traer_tarea(id_task: int):
    tarea = traer_tarea_por_id(id_task)
    if tarea is None:
        return {"error": "Tarea no encontrada"}
    return tarea

#Endpoint para borrar una tarea por id
@router.delete("/api/tasks/{id_task}", status_code=status.HTTP_200_OK, response_model=TareaResponse, dependencies=[Depends(JWTBearer())])
def borrar_tarea(id_task: int):
    tarea = borrar_tarea_por_id(id_task)
    if tarea is None:
        return {"error": "Tarea no encontrada"}
    return tarea