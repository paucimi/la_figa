FROM python:3.12-slim

WORKDIR /app

# Dependencias del sistema para ChromaDB
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY . .

# Cloud Run inyecta PORT; uvicorn lo usa
ENV PORT=8080
ENV CHROMA_DIR=/tmp/chroma_db
ENV SESSIONS_DIR=/tmp/sessions

EXPOSE 8080

CMD uvicorn ui.app:app --host 0.0.0.0 --port $PORT
