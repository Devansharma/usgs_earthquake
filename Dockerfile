FROM python:3.11-slim AS builder

ENV FLASK_DEBUG=1

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc \
    && rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip && \
    pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

FROM python:3.11-slim AS final

WORKDIR /app

COPY --from=builder /wheels /wheels

COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache /wheels/* && \
    addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser

COPY . .

ENV FLASK_DEBUG=1 \
    PYTHONUNBUFFERED=1

CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:create_app()","--log-level", "debug"]