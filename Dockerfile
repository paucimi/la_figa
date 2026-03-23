# ── Stage 1: Build React frontend ────────────────────────────────────────────
FROM node:20-slim AS frontend-builder

WORKDIR /frontend
COPY frontend/package.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# ── Stage 2: Python backend ───────────────────────────────────────────────────
FROM python:3.12-slim

WORKDIR /app

# Dependencias del sistema para ChromaDB y compilación
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libsqlite3-dev \
    sqlite3 \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY . .

# Copiar el build de React al directorio que FastAPI servirá
COPY --from=frontend-builder /frontend/dist ./ui/react_dist

# Cloud Run inyecta PORT; uvicorn lo usa
ENV PORT=8080
ENV CHROMA_DIR=/tmp/chroma_db
ENV SESSIONS_DIR=/tmp/sessions

# Vertex AI: en Cloud Run se usa ADC automático via Service Account
# No se necesita API key ni archivo de credenciales
ENV GOOGLE_GENAI_USE_VERTEXAI=1

EXPOSE 8080

CMD uvicorn ui.app:app --host 0.0.0.0 --port $PORT
