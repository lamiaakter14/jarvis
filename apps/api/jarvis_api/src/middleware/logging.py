"""Request logging middleware."""

import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Request/response logging middleware."""

    async def dispatch(self, request: Request, call_next):
        """Log request and response details."""
        start_time = time.time()

        # Log request
        logger.info(f"Request: {request.method} {request.url.path} " f"from {request.client.host}")

        # Process request
        response = await call_next(request)

        # Calculate processing time
        process_time = time.time() - start_time

        # Log response
        logger.info(f"Response: {response.status_code} " f"processed in {process_time:.3f}s")

        # Add custom header
        response.headers["X-Process-Time"] = str(process_time)

        return response
