from fastapi import FastAPI
from app.routers import visa

app = FastAPI(title="Servicio Visa", version="1.0.0")

app.include_router(visa.router, prefix="/visa", tags=["Visa"])