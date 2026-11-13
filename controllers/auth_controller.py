import hashlib
import secrets
from typing import Dict, Optional
from fastapi import HTTPException, status
from models.auth_model import LoginRequest, LoginResponse, UserInDB


class AuthController:
    """
    Controlador para la gestión de autenticación y seguridad.
    
    Aspectos de Ciberseguridad aplicados:
    1. Comparación en tiempo constante (Constant-Time Comparison):
       Uso de `secrets.compare_digest` para evitar ataques de canal lateral
       basados en tiempo (Timing Attacks).
    2. Mitigación de enumeración de usuarios:
       El mensaje de error no revela si falló el usuario o la contraseña.
    3. Validación y normalización del hash SHA-256 en minúsculas.
    """

    # Base de datos simulada en memoria
    # Hash SHA-256 de "lola123": cdd7acbd731138ebbe78080146e131a96282e9303270ba419f0b809c2f35f61f
    _USERS_DB: Dict[str, UserInDB] = {
        "admin": UserInDB(
            username="admin",
            password_hash=hashlib.sha256("lola123".encode("utf-8")).hexdigest()
        )
    }

    # Hash 'dummy' para realizar comparación en tiempo constante incluso si el usuario no existe,
    # evitando diferencias de tiempo de respuesta (User Enumeration mitigation)
    _DUMMY_HASH: str = hashlib.sha256(b"dummy_timing_protection_value").hexdigest()

    @classmethod
    def authenticate_user(cls, credentials: LoginRequest) -> LoginResponse:
        """
        Valida las credenciales recibidas comparando el hash recibido con el almacenado.
        Si las credenciales son válidas, retorna LoginResponse.
        Si no coinciden, lanza HTTPException 401 Unauthorized.
        """
        user_in_db: Optional[UserInDB] = cls._USERS_DB.get(credentials.user)

        # Si el usuario existe, comparamos con su hash; si no, comparamos con dummy para mitigar timing attacks
        target_hash = user_in_db.password_hash if user_in_db else cls._DUMMY_HASH

        # Normalizamos a minúsculas para consistencia de cadenas hexadecimales
        received_hash = credentials.password.strip().lower()
        
        # Comparación segura en tiempo constante
        is_password_valid = secrets.compare_digest(received_hash, target_hash)

        if not user_in_db or not is_password_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas: usuario o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return LoginResponse(
            status="success",
            message="Autenticación satisfactoria",
            user=user_in_db.username
        )
