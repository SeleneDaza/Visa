from fastapi import APIRouter

router = APIRouter()

TARJETAS_VISA = [
    {"numero_tarjeta": "4111111111111111", "cvv": "123"},
    {"numero_tarjeta": "4222222222222222", "cvv": "456"},
]

@router.post("/verificar-tarjeta")
def verificar_tarjeta(numero_tarjeta: str, cvv: str):
    for tarjeta in TARJETAS_VISA:
        if tarjeta["numero_tarjeta"] == numero_tarjeta and tarjeta["cvv"] == cvv:
            return {"existe": True, "mensaje": "Tarjeta verificada correctamente"}
    
    return {"existe": False, "mensaje": "Tarjeta no encontrada"}