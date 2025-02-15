# Procesador de Datasets con Flask y React

Esta aplicación permite procesar archivos CSV a través de una interfaz web amigable.

## Requisitos
- Docker
- Cuenta de Google Cloud Platform
- gcloud CLI

## Configuración Local
1. Clonar el repositorio
2. Configurar las variables de entorno:
   ```bash
   export GCS_BUCKET="nombre-del-bucket"
   export PROJECT_ID="id-del-proyecto"
   export GOOGLE_APPLICATION_CREDENTIALS="ruta/a/credentials.json"
   ```
3. Ejecutar con Docker Compose:
   ```bash
   docker-compose up --build
   ```