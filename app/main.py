from fastapi import FastAPI
from app.routers import visa
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Servicio Visa", version="1.0.0")

app.include_router(visa.router, prefix="/visa", tags=["Visa"])