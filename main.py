import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from views import api_router

app = FastAPI(
    title="API REST MVC - Ciberseguridad & FastAPI",
    description=(
        "API REST desarrollada bajo arquitectura MVC estricta con enfoque en Ciberseguridad.\n\n"
        "Endpoints disponibles:\n"
        "- `GET /health`: Monitoreo y estado del servicio.\n"
        "- `GET /catfact`: Consumo seguro y asíncrono de API externa con control de fallos.\n"
        "- `POST /login`: Autenticación con hash SHA-256 y protección contra Timing Attacks.\n"
        "- `POST /sum`: Operación aritmética tipada y validada estrictamente."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configuración de CORS segura
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción restringir a los dominios del cliente
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Inclusión de las rutas / vistas de la arquitectura MVC
app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
