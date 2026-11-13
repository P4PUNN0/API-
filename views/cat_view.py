from fastapi import APIRouter, status
from controllers.cat_controller import CatController
from models.cat_model import CatFactResponse

router = APIRouter()


@router.get(
    "/catfact",
    response_model=CatFactResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener un dato curioso de gatos",
    description="Consulta la API externa https://catfact.ninja/fact y devuelve el dato curioso obtenido."
)
async def get_cat_fact() -> CatFactResponse:
    """
    Vista/Endpoint que delega la petición HTTP externa al controlador CatController.
    """
    return await CatController.fetch_random_cat_fact()
