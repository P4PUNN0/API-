from pydantic import BaseModel, Field


class SumRequest(BaseModel):
    """
    Modelo de entrada para la operación suma.
    Garantiza que ambos operandos sean enteros estrictos.
    """
    a: int = Field(..., description="Primer número entero")
    b: int = Field(..., description="Segundo número entero")


class SumResponse(BaseModel):
    """
    Modelo de salida para el resultado de la suma: {"c": c}
    """
    c: int = Field(..., description="Resultado de la suma a + b")
