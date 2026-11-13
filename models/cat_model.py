from pydantic import BaseModel, Field


class CatFactResponse(BaseModel):
    """
    Modelo para la respuesta de un dato curioso de gatos.
    Mapea la respuesta devuelta por https://catfact.ninja/fact.
    """
    fact: str = Field(..., description="Curiosidad sobre gatos obtenida de la API externa")
    length: int = Field(..., description="Longitud del texto de la curiosidad")
