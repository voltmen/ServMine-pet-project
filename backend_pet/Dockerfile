FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get purge -y --auto-remove gcc libpq-dev

COPY . .

CMD ["python", "-m", "uvicorn", "testsAPI:app", "--host", "0.0.0.0", "--port", "8000"]