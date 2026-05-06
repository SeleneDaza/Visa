from sqlalchemy import Column, Integer, String
from app.database import Base

class TarjetaVisa(Base):
    __tablename__ = "tarjetas_visa"

    id = Column(Integer, primary_key=True, index=True)
    numero_tarjeta = Column(String(16), nullable=False, unique=True)
    cvv = Column(String(4), nullable=False)