# services/auth_service/app.py

from fastapi import FastAPI
from services.auth_service.routes import router as auth_router

app = FastAPI(
    title="Auth Service",
    description="Servicio de autenticación con registro, login y control de roles",
    version="1.0.0",
)

# Monta todas las rutas de auth bajo el prefijo /auth
app.include_router(auth_router)


# Ruta raíz de sanity check
@app.get("/")
def read_root():
    return {"message": "Auth Service"}
