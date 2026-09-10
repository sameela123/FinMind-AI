# FinMind AI Multi-Agent Production Dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PORT=8080 \
    APP_HOME=/app

WORKDIR $APP_HOME

# Copy application files
COPY data.json .
COPY backend/ ./backend/

# Install BigQuery client library
RUN pip install --no-cache-dir google-cloud-bigquery numpy

# Run native multi-agent API server
CMD ["python", "-m", "backend.main"]
