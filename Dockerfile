FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip (and basic build tooling)
RUN python -m pip install --upgrade pip setuptools wheel

# Copy project metadata first (for caching)
COPY pyproject.toml /app/
COPY README.md /app/
COPY LICENSE /app/

# Copy source code
COPY packages/ /app/packages/
COPY apps/ /app/apps/
COPY memory/ /app/memory/

# Install jarvis package (runtime)
RUN pip install -e .

# Create runtime directories
RUN mkdir -p /app/runtime/working \
             /app/runtime/metrics \
             /app/runtime/innovations \
             /app/runtime/cache \
             /app/runtime/working/execution_logs

# Copy configuration example
COPY .env.example /app/.env.example

ENV PYTHONPATH=/app/packages:/app/apps:$PYTHONPATH

EXPOSE 8000

CMD ["python", "-m", "jarvis_api.main"]
