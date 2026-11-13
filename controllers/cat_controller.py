import random
from typing import List
import httpx
from fastapi import HTTPException, status
from models.cat_model import CatFactResponse


class CatController:
    """
    Controlador para consumo de servicios externos.
    Maneja la resiliencia de red, timeouts, rate limiting y fallback local.
    """

    CAT_FACT_API_URL = "https://catfact.ninja/fact"
    TIMEOUT_SECONDS = 5.0

    # Lista local de respaldo para resiliencia ante Rate Limit (429) o Timeout en pruebas de carga
    _FALLBACK_FACTS: List[str] = [
        "Cats spend 70% of their lives sleeping.",
        "A cat has 32 muscles in each ear to control its movement.",
        "Cats have over 20 different vocalizations, including purrs, meows, and chirps.",
        "A cat cannot see directly under its nose.",
        "Cats have five toes on their front paws, but only four on the back.",
        "The first cat in space was a French cat named Félicette in 1963.",
        "A cat's purr vibrates at a frequency of 25 to 150 Hertz, which promotes bone and tissue healing.",
        "Cats can rotate their ears 180 degrees.",
        "A group of cats is called a clowder.",
        "Cats use their whiskers to detect if they can fit through a space."
    ]

    @classmethod
    def _get_random_fallback(cls) -> CatFactResponse:
        """Devuelve un dato de gato aleatorio desde la lista local de contingencia."""
        fact = random.choice(cls._FALLBACK_FACTS)
        return CatFactResponse(fact=fact, length=len(fact))

    @classmethod
    async def fetch_random_cat_fact(cls) -> CatFactResponse:
        """
        Realiza una petición HTTP GET asíncrona a la API de Cat Fact.
        
        Mecanismo de resiliencia (Graceful Degradation):
        - Si la API externa responde con HTTP 429 (Too Many Requests / Rate Limit)
          o la petición expira por Timeout, se activa el fallback local retornando
          código 200 con un dato aleatorio para garantizar la estabilidad durante Load Testing.
        """
        try:
            async with httpx.AsyncClient(timeout=cls.TIMEOUT_SECONDS) as client:
                response = await client.get(cls.CAT_FACT_API_URL)
                
                # Manejo específico si el servidor externo devuelve 429 (Rate Limit)
                if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
                    return cls._get_random_fallback()

                response.raise_for_status()
                data = response.json()
                
                return CatFactResponse(
                    fact=data.get("fact", "No fact available"),
                    length=data.get("length", len(data.get("fact", "")))
                )

        except httpx.TimeoutException:
            # Fallback en caso de timeout en la red para soportar pruebas de carga
            return cls._get_random_fallback()

        except httpx.HTTPStatusError as e:
            # En caso de que raise_for_status capture 429 u otros errores HTTP
            if e.response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
                return cls._get_random_fallback()
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"El servicio externo de Cat Fact respondió con error HTTP {e.response.status_code}."
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Fallo de conexión de red al consultar el servicio externo: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error inesperado al procesar la respuesta externa: {str(e)}"
            )
