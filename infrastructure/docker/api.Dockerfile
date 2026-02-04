# Multi-stage build for JARVIS API
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY apps/api/jarvis_api/requirements/base.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r base.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy wheels from builder
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy application
COPY packages/ /app/packages/
COPY apps/api/jarvis_api/ /app/apps/api/jarvis_api/
COPY memory/ /app/memory/
COPY runtime/ /app/runtime/

# Set Python path
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "apps.api.jarvis_api.src.main:app", "--host", "0.0.0.0", "--port", "8000"]
