from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """
    Modelo de entrada para la autenticación.
    user: Identificador del usuario (texto plano).
    password: Hash SHA-256 precalculado en el cliente (cadena hexadecimal de 64 caracteres).
    """
    user: str = Field(..., description="Nombre de usuario en texto plano", min_length=1, max_length=50)
    password: str = Field(
        ...,
        description="Contraseña pre-hasheada con SHA-256 por el cliente (64 caracteres hex)",
        min_length=64,
        max_length=64,
        pattern=r"^[a-fA-F0-9]{64}$"
    )


class LoginResponse(BaseModel):
    """
    Modelo de salida cuando la autenticación es exitosa (HTTP 200).
    """
    status: str = "success"
    message: str = "Autenticación satisfactoria"
    user: str


class UserInDB(BaseModel):
    """
    Representación interna de un usuario en el repositorio / base de datos.
    Almacena el hash SHA-256 de forma segura.
    """
    username: str
    password_hash: str
