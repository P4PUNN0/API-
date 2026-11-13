# API REST MVC con FastAPI y Ciberseguridad

API REST robusta construida con **Python 3** y **FastAPI**, implementando estrictamente el patrón de arquitectura **Modelo-Vista-Controlador (MVC)** y aplicando buenas prácticas de **Ciberseguridad**.

---

## 📁 Estructura de Directorios (MVC)

```text
API_ACT4/
│
├── models/                     # MODELO: Definición de datos, esquemas Pydantic y estructuras de dominio
│   ├── __init__.py
│   ├── auth_model.py           # Esquemas de entrada/salida para autenticación y modelo de usuario
│   ├── cat_model.py            # Esquema de respuesta para Cat Fact
│   ├── health_model.py         # Esquema de estado para /health
│   └── math_model.py           # Esquema de entrada y salida para /sum
│
├── controllers/                # CONTROLADOR: Lógica de negocio, consumo de APIs y validaciones
│   ├── __init__.py
│   ├── auth_controller.py      # Autenticación, comparación en tiempo constante (Anti-Timing Attacks)
│   ├── cat_controller.py       # Petición HTTP asíncrona a https://catfact.ninja/fact con manejo de errores
│   └── math_controller.py      # Lógica de cálculo aritmético c = a + b
│
├── views/                      # VISTA (Rutas / Endpoints): Exposición de la interfaz HTTP REST
│   ├── __init__.py             # Agrupador de routers (api_router)
│   ├── auth_view.py            # Endpoint POST /login
│   ├── cat_view.py             # Endpoint GET /catfact
│   ├── health_view.py          # Endpoint GET /health
│   └── math_view.py            # Endpoint POST /sum
│
├── main.py                     # Punto de entrada de la aplicación y configuración de FastAPI
├── requirements.txt            # Dependencias del proyecto
├── generate_hash.py            # Script utilitario para generar hashes SHA-256
└── README.md                   # Documentación y guía de pruebas
```

---

## 🔒 Consideraciones de Ciberseguridad Implementadas

1. **Mitigación de Ataques de Canal Lateral por Tiempo (Timing Attacks):**
   - En lugar de usar el operador estándar `==` para comparar los hashes (el cual se interrumpe en el primer carácter discrepante), se utiliza `secrets.compare_digest()`. Esto garantiza una comparación en **tiempo constante**, impidiendo que un atacante deduzca la contraseña analizando fluctuaciones en milisegundos.
2. **Mitigación de Enumeración de Usuarios (User Enumeration):**
   - Si el usuario no existe en la base de datos, el sistema realiza igualmente una comparación contra un hash simulado (*dummy hash*) y devuelve un mensaje genérico (`Credenciales inválidas`), evitando revelar si el fallo provino del usuario o de la contraseña.
3. **Validación Estricta de Entradas (Pydantic):**
   - El hash recibido debe cumplir estrictamente con una cadena hexadecimal de 64 caracteres (`^[a-fA-F0-9]{64}$`), previniendo inyecciones o datos malformados.
   - En la suma, `a` y `b` son forzados a ser enteros puros.
4. **Resiliencia de Red, Timeouts y Fallback Local (Degradación Elegante):**
   - La llamada externa a `https://catfact.ninja/fact` se ejecuta de forma asíncrona (`httpx.AsyncClient`) con un tiempo de espera de 5 segundos (`timeout`).
   - Para soportar **pruebas de carga (Load Testing)** y evitar fallos por saturación en la red o por límite de peticiones del proveedor externo (**HTTP 429 Too Many Requests** o **Timeout**), el controlador activa automáticamente un fallback local con código **HTTP 200** seleccionando un dato curioso aleatorio de una lista en memoria.

---

## 🚀 Instalación y Puesta en Marcha

### 1. Crear entorno virtual e instalar dependencias

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
# En Linux/macOS:
source venv/bin/activate
# En Windows:
# venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Ejecutar el servidor

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
O directamente con Python:
```bash
python3 main.py
```

La API quedará escuchando en `http://localhost:8000`.  
Documentación interactiva disponible en:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 🔑 Cálculo del Hash SHA-256 de "lola123"

### Opción 1: Con el script incluido
```bash
python3 generate_hash.py lola123
```

### Opción 2: Comando directo de terminal (One-Liner)
```bash
python3 -c 'import hashlib; print(hashlib.sha256(b"lola123").hexdigest())'
```

**Resultado:**
```text
cdd7acbd731138ebbe78080146e131a96282e9303270ba419f0b809c2f35f61f
```

---

## 📡 Pruebas de Endpoints (Postman / cURL)

### 1. `GET /health`
Verifica que el servicio esté activo.
- **Método:** `GET`
- **URL:** `http://localhost:8000/health`
- **Respuesta esperada (HTTP 200 OK):**
```json
{
  "status": "ok"
}
```

---

### 2. `GET /catfact`
Consulta externa a la API de Cat Fact.
- **Método:** `GET`
- **URL:** `http://localhost:8000/catfact`
- **Respuesta esperada (HTTP 200 OK):**
```json
{
  "fact": "A cat's hearing is much more sensitive than humans and dogs.",
  "length": 60
}
```

---

### 3. `POST /login`
Autenticación de usuario.

#### Caso Exitoso:
- **Método:** `POST`
- **URL:** `http://localhost:8000/login`
- **Headers:** `Content-Type: application/json`
- **Body (raw JSON):**
```json
{
  "user": "admin",
  "password": "cdd7acbd731138ebbe78080146e131a96282e9303270ba419f0b809c2f35f61f"
}
```
- **Respuesta esperada (HTTP 200 OK):**
```json
{
  "status": "success",
  "message": "Autenticación satisfactoria",
  "user": "admin"
}
```

#### Caso Fallido (Credenciales inválidas):
- **Body (raw JSON):**
```json
{
  "user": "admin",
  "password": "0000000000000000000000000000000000000000000000000000000000000000"
}
```
- **Respuesta esperada (HTTP 401 Unauthorized):**
```json
{
  "detail": "Credenciales inválidas: usuario o contraseña incorrectos"
}
```

---

### 4. `POST /sum`
Calcula `c = a + b`.
- **Método:** `POST`
- **URL:** `http://localhost:8000/sum`
- **Headers:** `Content-Type: application/json`
- **Body (raw JSON):**
```json
{
  "a": 15,
  "b": 27
}
```
- **Respuesta esperada (HTTP 200 OK):**
```json
{
  "c": 42
}
```


---

## 🛡️ Auditoría de Seguridad con Agente IA

Esta API fue auditada automáticamente por un **Agente de IA especializado en ciberseguridad** que realizó análisis de código estático y pruebas dinámicas.

👉 **Repositorio del Agente Auditor:** [AGENTE-IA](https://github.com/P4PUNN0/AGENTE-IA)

El agente identificó **7 hallazgos** (0 críticos, 0 altos) y validó las buenas prácticas de seguridad implementadas en esta API, incluyendo:
- ✅ `secrets.compare_digest()` para prevención de timing attacks
- ✅ Validación estricta de entradas con Pydantic
- ✅ Mitigación de enumeración de usuarios
- ✅ Resiliencia de red con fallback local
- ✅ Documentación automática con Swagger/ReDoc

---

## 📚 Materia

**Ciberseguridad** — Tecmilenio
