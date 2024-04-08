from fastapi import APIRouter, status
from dtos import PilotoDto, PilotoResponse
from servicios import crear_piloto_svc, traer_pilotos_svc

router = APIRouter()

@router.get("/pilotos", status_code=status.HTTP_200_OK)
def traer_pilotos():
    pilotos = traer_pilotos_svc()
    return pilotos    

@router.post("/pilotos", status_code=status.HTTP_201_CREATED)
def crear_piloto(piloto: PilotoDto) -> PilotoResponse:
    piloto = crear_piloto_svc(piloto)
    return piloto