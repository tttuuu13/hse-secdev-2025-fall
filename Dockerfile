FROM python:3.11.8-alpine3.19 AS build
WORKDIR /app

COPY requirements.txt ./

# Update OS packages and setuptools to fix known vulnerabilities
RUN apk upgrade --no-cache && \
    pip install --no-cache-dir --upgrade setuptools==68.2.2 && \
    pip wheel --no-cache-dir --wheel-dir=/wheels -r requirements.txt

FROM python:3.11.8-alpine3.19 AS runtime
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

RUN addgroup -S appuser && adduser -S -G appuser appuser

COPY --from=build /wheels /wheels

RUN pip install --no-cache-dir /wheels/* && \
    rm -rf /wheels


COPY . .

RUN chown -R appuser:appuser /app

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c 'import urllib.request; urllib.request.urlopen("http://localhost:8000/health")'
USER appuser
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
