from fastapi import APIRouter, status
from models.health_model import HealthResponse

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check del servicio",
    description="Regresa código HTTP 200 con {'status': 'ok'} para monitoreo de disponibilidad."
)
async def check_health() -> HealthResponse:
    """
    Vista/Endpoint para verificar el estado de salud de la API.
    """
    return HealthResponse(status="ok")
