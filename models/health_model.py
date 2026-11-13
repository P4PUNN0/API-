from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """
    Modelo de respuesta para verificación del estado del servicio.
    """
    status: str = Field("ok", description="Estado operativo de la API")
