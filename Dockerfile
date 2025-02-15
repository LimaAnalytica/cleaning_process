# Build frontend
FROM node:16-slim as frontend-builder

WORKDIR /app/frontend
COPY frontend/package*.json ./

# Asegurar permisos para npm
RUN mkdir -p /app/frontend/node_modules && \
    chown -R node:node /app/frontend

# Cambiar al usuario node
USER node

RUN npm install
COPY --chown=node:node frontend/ ./
RUN npm run build

# Build backend
FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && \
    apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/*

# Copiar y instalar requisitos del backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade Flask Werkzeug
RUN pip install flask-cors

# Copiar el backend
COPY backend/ .

# Copiar el frontend construido desde la etapa anterior
COPY --from=frontend-builder /app/frontend/build /app/static

# Configurar nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Script de inicio
RUN echo '#!/bin/bash\nservice nginx start\npython -m app.main &\nwait -n' > /start.sh && \
    chmod +x /start.sh

EXPOSE 9090

CMD ["/start.sh"]