"""FastAPI main application for JARVIS cognitive assistant - Enhanced Version."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .api import v1_router, v2_router
from .config import settings, setup_logging
from .middleware import LoggingMiddleware, RateLimitMiddleware, setup_cors, setup_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    setup_logging()
    yield
    # Shutdown


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="AI-powered cognitive assistant with multi-agent architecture",
    version=settings.app_version,
    lifespan=lifespan,
)

# Setup middleware
setup_cors(app)
setup_exception_handlers(app)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware, rate_limit=settings.rate_limit_per_minute)

# Include routers
app.include_router(v1_router, prefix=settings.api_v1_prefix)
app.include_router(v2_router, prefix="/api/v2")


@app.get("/")
async def root():
    """Root endpoint."""
    return JSONResponse(
        content={
            "message": settings.app_name,
            "version": settings.app_version,
            "status": "running",
            "api_versions": {"v1": settings.api_v1_prefix, "v2": "/api/v2"},
        }
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=settings.debug)
