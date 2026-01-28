# ---- Builder Stage ----
FROM python:3.11-slim-bookworm as builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ---- Runtime Stage ----
FROM python:3.11-slim-bookworm

WORKDIR /usr/src/app

# Set production environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

RUN addgroup --system app && adduser --system --group app
USER app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY --chown=app:app . .

EXPOSE 8080

# Increased timeout and explicit logging for Cloud Run
CMD ["gunicorn", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "app.main:app", \
     "--bind", "0.0.0.0:8080", \
     "--workers", "1", \
     "--timeout", "90", \
     "--keep-alive", "5", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "debug"]