from fastapi import APIRouter, status
from dtos.authentication import SignUpRequest, User
from dtos import PilotoResponse, PilotoDto
from servicios import crear_piloto_svc, traer_pilotos_svc, autenticar_piloto_svc

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