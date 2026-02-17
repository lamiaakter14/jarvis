"""Security headers middleware for API protection."""

from fastapi import Request
from fastapi.responses import Response


async def security_headers_middleware(request: Request, call_next) -> Response:
    """Add security headers to all responses.

    Implements OWASP security best practices for HTTP headers.

    Args:
        request: FastAPI request object
        call_next: Next middleware/endpoint to call

    Returns:
        Response with security headers added
    """
    response = await call_next(request)

    # Prevent clickjacking attacks
    response.headers["X-Frame-Options"] = "DENY"

    # Prevent MIME type sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"

    # Enable XSS protection
    response.headers["X-XSS-Protection"] = "1; mode=block"

    # Strict Transport Security (HTTPS only)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

    # Content Security Policy
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self' data:; "
        "connect-src 'self' ws: wss:; "
        "frame-ancestors 'none';"
    )

    # Referrer Policy
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    # Permissions Policy
    response.headers["Permissions-Policy"] = (
        "geolocation=(), " "microphone=(), " "camera=(), " "payment=(), " "usb=()"
    )

    # Remove server header to avoid information disclosure
    response.headers.pop("Server", None)

    return response
