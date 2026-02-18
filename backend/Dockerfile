FROM python:3.12-slim

# Poppler requis par pdf2image pour la conversion PDF → PNG
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Le code source est monté en volume (dev) — pas de COPY .
# Hot reload activé via --reload
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
