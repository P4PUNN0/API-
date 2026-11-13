from models.math_model import SumRequest, SumResponse


class MathController:
    """
    Controlador para operaciones matemáticas y lógica de negocio aritmética.
    """

    @classmethod
    def calculate_sum(cls, payload: SumRequest) -> SumResponse:
        """
        Calcula la suma c = a + b y retorna el modelo tipado.
        """
        total = payload.a + payload.b
        return SumResponse(c=total)
