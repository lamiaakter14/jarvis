# JARVIS Cognitive Assistant - Dockerfile
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy packages
COPY packages/ /app/packages/

# Copy apps
COPY apps/api/ /app/apps/api/
COPY apps/cli/ /app/apps/cli/

# Copy configuration
COPY .env.example /app/.env.example
COPY pyproject.toml /app/

# Create runtime directory
RUN mkdir -p /app/runtime/working/execution_logs /app/runtime/metrics /app/runtime/innovations /app/runtime/cache

# Copy memory (curated knowledge)
COPY memory/ /app/memory/

# Expose port for API
EXPOSE 8000

# Set Python path
ENV PYTHONPATH=/app/packages:/app/apps/api:/app/apps/cli

# Default command (API server)
CMD ["python", "-m", "uvicorn", "jarvis_api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Alternative commands:
# - CLI: docker run jarvis python -m jarvis_cli.main --help

