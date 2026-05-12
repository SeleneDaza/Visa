from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import TarjetaVisa

router = APIRouter()

@router.post("/verificar-tarjeta")
def verificar_tarjeta(numero_tarjeta: str, cvv: str, db: Session = Depends(get_db)):
    tarjeta = db.query(TarjetaVisa).filter(
        TarjetaVisa.numero_tarjeta == numero_tarjeta,
        TarjetaVisa.cvv == cvv
    ).first()

    if tarjeta:
        return {"existe": True, "mensaje": "Tarjeta verificada correctamente"}
    
    return {"existe": False, "mensaje": "Tarjeta no encontrada"}