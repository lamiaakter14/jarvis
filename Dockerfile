FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy packages (core logic)
COPY packages/ /app/packages/

# Copy pyproject.toml for package installation
COPY pyproject.toml /app/

# Install jarvis package
RUN pip install -e .

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
ENV PYTHONPATH=/app/packages:/app/apps:$PYTHONPATH

# Expose API port
EXPOSE 8000

# Default command: run API
CMD ["python", "-m", "jarvis_api.main"]
