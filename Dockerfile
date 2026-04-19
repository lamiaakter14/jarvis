FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install build tools
RUN python -m pip install --upgrade pip setuptools wheel

# Copy project metadata and install Python dependencies
COPY pyproject.toml /app/
COPY README.md /app/

# Copy packages (core logic)
COPY packages/ /app/packages/

# Install jarvis package and all runtime dependencies
RUN pip install --no-cache-dir -e .

# Copy apps
COPY apps/ /app/apps/

# Copy memory (curated knowledge)
COPY memory/ /app/memory/

# Create runtime directory structure
RUN mkdir -p /app/runtime/working \
             /app/runtime/metrics \
             /app/runtime/innovations \
             /app/runtime/cache \
             /app/runtime/working/execution_logs

# Copy configuration
COPY .env.example /app/.env.example

# Set Python path
ENV PYTHONPATH=/app/packages:/app/apps/api:$PYTHONPATH

# Expose API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Default command: run API
CMD ["python", "-m", "jarvis_api.main"]

