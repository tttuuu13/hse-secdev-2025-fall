FROM python:3.11.8-alpine3.19 AS build
WORKDIR /app

COPY requirements.txt ./


RUN apk upgrade --no-cache && \
    pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip wheel --no-cache-dir --wheel-dir=/wheels -r requirements.txt

FROM python:3.11.8-alpine3.19 AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN addgroup -S appuser && adduser -S -G appuser appuser

RUN apk upgrade --no-cache

COPY --from=build /wheels /wheels

RUN pip install --no-cache-dir --upgrade pip setuptools && \
    pip install --no-cache-dir /wheels/* && \
    rm -rf /wheels

COPY --chown=appuser:appuser . .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c 'import urllib.request; urllib.request.urlopen("http://localhost:8000/health")'

USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
