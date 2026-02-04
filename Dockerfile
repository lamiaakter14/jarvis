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

# Copy application code
COPY . .

# Create memory directory
RUN mkdir -p memory/working memory/knowledge memory/strategic

# Expose port for API
EXPOSE 8000

# Set Python path
ENV PYTHONPATH=/app

# Default command (API server)
CMD ["python", "src/presentation/api/main.py"]

# Alternative commands:
# - CLI: docker run jarvis python src/presentation/cli/main.py --help
# - Legacy: docker run jarvis python scripts/test_cognitive_loop.py
