from fastapi import APIRouter, status
from controllers.math_controller import MathController
from models.math_model import SumRequest, SumResponse

router = APIRouter()


@router.post(
    "/sum",
    response_model=SumResponse,
    status_code=status.HTTP_200_OK,
    summary="Suma de dos números enteros",
    description="Recibe {a: int, b: int}, calcula c = a + b y retorna {c: c} con código HTTP 200."
)
async def sum_numbers(payload: SumRequest) -> SumResponse:
    """
    Vista/Endpoint que procesa la suma aritmética delegando en MathController.
    """
    return MathController.calculate_sum(payload)
