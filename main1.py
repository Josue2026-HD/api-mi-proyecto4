# --- main.py (cabecera) ---
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# --- main.py (Endpoint Health Check) ---
@app.get("/health", tags=["Sistema"])
def health_check():
    return {
        "status": "online",
        "ambiente": os.getenv("ENVIRONMENT", "desarrollo_local"),
        "servidor": "FastAPI + Uvicorn Cloud"
    }

# --- main.py (Bloque de arranque productivo) ---
if __name__ == "__main__":
    import uvicorn
    # Lee el puerto inyectado por el PaaS; si no existe, usa 8000 por defecto
    puerto = int(os.environ.get("PORT", 8000))
    # Escucha obligatoria en 0.0.0.0 para entornos en la nube
    uvicorn.run("main:app", host="0.0.0.0", port=puerto, reload=False)

# --- main.py (Nuevo endpoint versión) ---
@app.get("/version", tags=["Sistema"])
def consultar_version():
    return {
        "version": "1.2.0",
        "descripcion": "API desplegada mediante Continuous Deployment desde GitHub",
        "docente": "Lic. Ronald J. Villar Gonzales",
        "institucion": "IES República Federal de Alemania - Chiclayo"
    }

# --- main.py (Lectura de Variables de Entorno) ---
from dotenv import load_dotenv

# Carga las variables del archivo .env local si existe
load_dotenv()

SECRET_KEY = os.getenv("API_SECRET_KEY", "clave_por_defecto_insegura")
MODO_DEBUG = os.getenv("MODO_DEBUG", "False")

@app.get("/config-check", tags=["Seguridad"])

def config_check():
    return {
        "modo_debug": MODO_DEBUG,
        # Buena práctica: nunca reveles el valor completo del secreto en logs o endpoints
        "clave_configurada": True if SECRET_KEY != "clave_por_defecto_insegura" else False,
        "prefijo_clave": SECRET_KEY[:4] + "****"
    }

# --- main.py (Endpoint con error intencional) ---
@app.get("/simular-error", tags=["Diagnóstico"])
def simular_error():
    # División por cero: provocará una excepción no controlada
    resultado = 10 / 0
    return {"resultado": resultado}

# --- main.py (Configuración de CORS) ---
from fastapi.middleware.cors import CORSMiddleware

# Configuración de orígenes permitidos
origins = [
    "*",  # En fase de desarrollo/aprendizaje permite cualquier origen. En empresas se especifica el dominio exacto.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

