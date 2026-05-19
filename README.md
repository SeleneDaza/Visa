# Visa Function — Serverless

Función serverless desarrollada con Azure Functions y Python que verifica
si una tarjeta Visa existe en la base de datos.

## Tecnologías
- Python 3.13
- Azure Functions Core Tools v4
- PostgreSQL (Docker)

## Requisitos previos
- Python 3.13
- Docker Desktop
- Node.js v18+
- Azure Functions Core Tools v4:
  npm install -g azure-functions-core-tools@4 --unsafe-perm true

## Configuración

1. Clona el repositorio
2. Instala dependencias:
   pip install --target=".python_packages/lib/site-packages" psycopg2-binary azure-functions

3. Copia el archivo de variables de entorno:
   copy .env.example local.settings.json

## Ejecución

### 1. Levanta la base de datos
   docker-compose up

### 2. Crea la tabla (solo primera vez)
   docker exec -it visa-visa-db-1 psql -U visa_user -d visa_db -c "CREATE TABLE tarjetas_visa (id SERIAL PRIMARY KEY, numero_tarjeta VARCHAR(16) NOT NULL UNIQUE, cvv VARCHAR(4) NOT NULL);"

### 3. Inserta datos de prueba (solo primera vez)
   docker exec -it visa-visa-db-1 psql -U visa_user -d visa_db -c "INSERT INTO tarjetas_visa (numero_tarjeta, cvv) VALUES ('4111111111111111', '123'), ('4222222222222222', '456'), ('4333333333333333', '789');"

### 4. Levanta la función
   func start

La función estará disponible en: http://localhost:7071/api/verificar-tarjeta

## Endpoint

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | /api/verificar-tarjeta | Verifica si una tarjeta Visa existe |

### Body JSON
```json
{
  "numero_tarjeta": "4111111111111111",
  "cvv": "123"
}
```

### Respuesta exitosa
```json
{"existe": true, "mensaje": "Tarjeta verificada correctamente"}
```

### Respuesta fallida
```json
{"existe": false, "mensaje": "Tarjeta no encontrada"}
```

### Respuesta error
```json
{"existe": false, "mensaje": "Error interno del servicio"}
```

## Variables de entorno

| Variable | Descripción |
|----------|-------------|
| DATABASE_URL | URL de conexión a PostgreSQL |

## Prueba rápida
curl -X POST http://localhost:7071/api/verificar-tarjeta \
  -H "Content-Type: application/json" \
  -d "{\"numero_tarjeta\": \"4111111111111111\", \"cvv\": \"123\"}"