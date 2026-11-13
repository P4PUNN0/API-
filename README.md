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

## 📸 Capturas de Pruebas de Carga (Load Testing con Postman)

Se realizaron múltiples pruebas de carga utilizando **Postman Performance Testing** para evaluar el comportamiento de la API bajo distintos escenarios de estrés. A continuación se documentan los resultados:

---

### 🔹 Prueba #1 — Perfil Fijo, 5 VUs (Línea Base)

![Prueba de carga #1 - Línea base con 5 usuarios virtuales](CAPTURAS/swappy-20261111_183224.png)

**Configuración:** 5 usuarios virtuales (VUs) | Perfil fijo | ~2 minutos

**Resultados clave:**
- **4,628 peticiones totales** a ~9.56 req/s por endpoint
- **0% de errores** en los 4 endpoints
- `GET /health`: 6 ms promedio (P99: 42 ms) — respuesta casi instantánea
- `POST /login`: 6 ms promedio (P99: 37 ms) — autenticación eficiente
- `POST /sum`: 6 ms promedio (P99: 42 ms) — cálculo rápido
- `GET /catfact`: 1,415 ms promedio (P99: 5,575 ms) — latencia esperada por la dependencia de API externa

> ✅ **Conclusión:** La API opera de forma estable con carga baja. La latencia del endpoint `/catfact` es inherente a la llamada HTTP externa a `catfact.ninja`.

---

### 🔹 Prueba #2 — Perfil Fijo, 20 VUs (Carga Media)

![Prueba de carga #2 - 20 usuarios virtuales, perfil fijo](CAPTURAS/swappy-20261111_183842.png)

**Configuración:** 20 usuarios virtuales | Perfil fijo | 5 minutos

**Resultados clave:**
- **23,580 peticiones totales** a 78.52 req/s
- **0% de errores** y **0% de fallos** en todos los endpoints
- Tiempo de respuesta promedio: **242 ms** (P90: 782 ms, P99: 3,050 ms)
- `GET /health`: 9 ms promedio — estable bajo presión
- `GET /catfact`: 927 ms promedio — el fallback local se activa ante rate limiting
- `POST /sum` y `POST /login`: 27 ms y 8 ms promedio respectivamente
- **Peak CPU: 52.2%** | **Peak Memory: 64.0%** — recursos bajo control

> ✅ **Conclusión:** La API escala correctamente a 20 VUs. El mecanismo de **Graceful Degradation** del endpoint `/catfact` funciona correctamente activando el fallback local cuando la API externa limita las peticiones.

---

### 🔹 Prueba #3 — Perfil Spike, 20 VUs (Picos de Carga)

![Prueba de carga #3 - Perfil spike con picos repentinos](CAPTURAS/swappy-20261111_184136.png)

**Configuración:** 20 usuarios virtuales | Perfil Spike | 2 minutos

**Resultados clave:**
- **980 peticiones totales** a 8.15 req/s
- **0% de errores** — la API absorbe los picos sin fallar
- Tiempo de respuesta promedio: **425 ms** (P90: 1,553 ms, P99: 4,449 ms)
- Se observa un pico de latencia a las 18:40:08 (~5,445 ms) coincidiendo con el spike de usuarios
- `GET /catfact` alcanza hasta 7,175 ms en pico — el timeout de 5s se activa y el fallback responde
- **Peak CPU: 30.0%** | **Peak Memory: 60.1%**

> ✅ **Conclusión:** El perfil Spike confirma que la API maneja ráfagas repentinas de tráfico sin errores. La degradación elegante protege la disponibilidad del servicio.

---

### 🔹 Prueba #4 — Perfil Spike, 20 VUs, 5 minutos (Spike Sostenido)

![Prueba de carga #4 - Spike sostenido durante 5 minutos](CAPTURAS/swappy-20261111_184707.png)

**Configuración:** 20 usuarios virtuales | Perfil Spike | 5 minutos

**Resultados clave:**
- **5,118 peticiones totales** a 17.04 req/s
- **0% de errores** | **0% de fallos**
- Tiempo de respuesta promedio: **212 ms** (P90: 647 ms, P95: 936 ms)
- Comparación con ejecución anterior: ⬇️ Avg. response time 12.4% | ⬇️ P95 13.7%
- `GET /catfact`: 827 ms promedio con Max de 5,595 ms — se estabiliza con fallback
- **Peak CPU: 44.7%** | **Peak Memory: 62.4%**

> ✅ **Conclusión:** En una prueba Spike más larga, la API mejora su rendimiento conforme se estabiliza. Los tiempos de respuesta bajan comparados con la ejecución anterior, demostrando consistencia.

---

### 🔹 Prueba #5 — Perfil Fijo, 20 VUs, 7 minutos (Carga Sostenida Máxima)

![Prueba de carga #5 - Carga máxima sostenida 7 minutos](CAPTURAS/swappy-20261111_185429.png)

**Configuración:** 20 usuarios virtuales | Perfil fijo | 7 minutos

**Resultados clave:**
- **35,007 peticiones totales** a **83.28 req/s** — máximo throughput alcanzado
- **0% de errores** | **0% de fallos**
- Tiempo de respuesta promedio: **229 ms** (P90: 715 ms, P99: 3,102 ms)
- Comparación con ejecución anterior: ⬆️ Requests/second **388.7%** de mejora
- `GET /health`: 7 ms promedio | `POST /login`: mantiene estabilidad
- **Peak CPU: 41.8%** | **Peak Memory: 62.0%**

> ✅ **Conclusión:** La prueba de mayor duración y carga confirma que la API es **robusta y escalable**. Con 35,000+ peticiones procesadas sin un solo error, el sistema demuestra estar listo para producción académica.

---

### 🔹 Prueba #6 — API MVC Original (http.server), 20 VUs, 5 minutos

![Prueba de carga #6 - API original con http.server de Python](CAPTURAS/WhatsApp%20Image%202026-11-11%20at%2018.42.48.jpeg)

**Configuración:** 20 usuarios virtuales | Perfil fijo | 5 minutos | API MVC original (http.server)

**Resultados clave:**
- **72,040 peticiones totales** a **148.15 req/s**
- **Error %: 62.73%** — tasa de errores muy alta
- `GET New Request` y `GET Health`: **100% de errores** (respuestas no conformes al esquema esperado)
- `POST /login` y `POST /sum`: **~6.8% de errores**
- Tiempo de respuesta promedio: **8 ms** (muy rápido pero con errores)
- **Peak CPU: 90.5%** | **Peak Memory: 93.0%** — recursos al límite

> ⚠️ **Conclusión:** La API original basada en `http.server` es rápida en respuesta bruta pero **no maneja correctamente la carga**: alta tasa de errores, CPU al 90% y memoria al 93%. Esto justifica la migración a FastAPI.

---

### 🔹 Prueba #7 — API MVC Original (http.server), 20 VUs, 7 minutos

![Prueba de carga #7 - API original bajo estrés prolongado](CAPTURAS/WhatsApp%20Image%202026-11-11%20at%2018.49.46.jpeg)

**Configuración:** 20 usuarios virtuales | Perfil fijo | 7 minutos | API MVC original (http.server)

**Resultados clave:**
- **12,420 peticiones totales** a **100.87 req/s**
- **Error %: 60.09%** — errores persistentes
- Endpoints GET: **100% de errores**
- Tiempo de respuesta promedio: **18 ms**
- **Peak CPU: 99.2%** | **Peak Memory: 94.7%** — sistema casi colapsado

> ⚠️ **Conclusión:** Bajo estrés prolongado, la API original consume casi el **100% del CPU** y **95% de memoria**, confirmando que `http.server` de Python no es adecuado para cargas de producción. La versión con FastAPI demostró ser significativamente más estable y eficiente.

---

### 📊 Tabla Comparativa: FastAPI vs http.server

| Métrica | FastAPI (Prueba #5) | http.server (Prueba #7) |
|---------|:-------------------:|:-----------------------:|
| Total de peticiones | 35,007 | 12,420 |
| Requests/segundo | 83.28 | 100.87 |
| Error % | **0.00%** | **60.09%** |
| Failure % | **0.00%** | 0.00% |
| Avg. Response Time | 229 ms | 18 ms |
| Peak CPU % | **41.8%** | **99.2%** |
| Peak Memory % | **62.0%** | **94.7%** |

> 💡 **Veredicto:** Aunque `http.server` tiene menor latencia bruta, **FastAPI gana en confiabilidad, eficiencia de recursos y cero errores bajo carga**. La arquitectura asíncrona de FastAPI con uvicorn es la elección correcta para aplicaciones que requieren resiliencia.

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
