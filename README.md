# Servicio Visa - REST API

Microservicio independiente desarrollado en Python/FastAPI que verifica
si una tarjeta Visa existe en la base de datos.

## Tecnologías
- Python 3.13
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker / Docker Compose

## Estructura del proyecto
visa-service/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── routers/
│       ├── __init__.py
│       └── visa.py
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
└── README.md

## Configuración

1. Clona el repositorio
2. Copia el archivo de variables de entorno:
cp .env.example .env
3. Edita `.env` con tus credenciales reales

## Ejecución con Docker

docker-compose up --build

El servicio estará disponible en: http://localhost:8000

## Endpoint

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | /visa/verificar-tarjeta | Verifica si una tarjeta Visa existe |

### Parámetros
| Campo | Tipo | Descripción |
|-------|------|-------------|
| numero_tarjeta | string | Número de 16 dígitos |
| cvv | string | Código de seguridad |

### Respuesta exitosa
```json
{"existe": true, "mensaje": "Tarjeta verificada correctamente"}
```

### Respuesta fallida
```json
{"existe": false, "mensaje": "Tarjeta no encontrada"}
```

## Documentación interactiva
http://localhost:8000/docs