from fastapi import APIRouter, status
from controllers.auth_controller import AuthController
from models.auth_model import LoginRequest, LoginResponse

router = APIRouter()


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Autenticación exitosa"},
        401: {"description": "Credenciales inválidas"},
        422: {"description": "Entidad no procesable (error de validación de esquema)"}
    },
    summary="Inicio de sesión con hash SHA-256",
    description=(
        "Recibe un usuario en texto plano y una contraseña pre-hasheada en SHA-256 por el cliente. "
        "Verifica contra el almacén seguro mediante comparación en tiempo constante."
    )
)
async def login(credentials: LoginRequest) -> LoginResponse:
    """
    Vista/Endpoint que procesa la solicitud de login delegando en AuthController.
    """
    return AuthController.authenticate_user(credentials)
