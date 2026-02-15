"""Rate limiting middleware for API endpoints."""

from typing import Dict, Optional
from datetime import datetime, timedelta
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import time


class RateLimiter:
    """In-memory rate limiter for API endpoints.
    
    Implements token bucket algorithm for rate limiting.
    For production, consider using Redis-based rate limiting.
    """
    
    def __init__(
        self,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000
    ):
        """Initialize rate limiter.
        
        Args:
            requests_per_minute: Maximum requests per minute per client
            requests_per_hour: Maximum requests per hour per client
        """
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        
        # Store request history: {client_id: [(timestamp, count), ...]}
        self._minute_buckets: Dict[str, list] = {}
        self._hour_buckets: Dict[str, list] = {}
    
    def _get_client_id(self, request: Request) -> str:
        """Extract client identifier from request.
        
        Args:
            request: FastAPI request object
            
        Returns:
            Client identifier (IP address or API key)
        """
        # Try to get API key from headers
        api_key = request.headers.get("X-API-Key")
        if api_key:
            return f"api_key:{api_key}"
        
        # Fall back to IP address
        client_ip = request.client.host if request.client else "unknown"
        return f"ip:{client_ip}"
    
    def _clean_old_entries(
        self,
        bucket: Dict[str, list],
        max_age_seconds: int
    ) -> None:
        """Remove old entries from rate limit bucket.
        
        Args:
            bucket: Rate limit bucket to clean
            max_age_seconds: Maximum age of entries to keep
        """
        current_time = time.time()
        cutoff_time = current_time - max_age_seconds
        
        for client_id in list(bucket.keys()):
            # Filter out old entries
            bucket[client_id] = [
                (ts, count) for ts, count in bucket[client_id]
                if ts > cutoff_time
            ]
            
            # Remove empty buckets
            if not bucket[client_id]:
                del bucket[client_id]
    
    def _check_limit(
        self,
        client_id: str,
        bucket: Dict[str, list],
        max_requests: int,
        window_seconds: int
    ) -> tuple[bool, int]:
        """Check if client has exceeded rate limit.
        
        Args:
            client_id: Client identifier
            bucket: Rate limit bucket
            max_requests: Maximum allowed requests
            window_seconds: Time window in seconds
            
        Returns:
            Tuple of (is_allowed, remaining_requests)
        """
        current_time = time.time()
        cutoff_time = current_time - window_seconds
        
        # Get client's request history
        if client_id not in bucket:
            bucket[client_id] = []
        
        # Count recent requests
        recent_requests = sum(
            count for ts, count in bucket[client_id]
            if ts > cutoff_time
        )
        
        is_allowed = recent_requests < max_requests
        remaining = max(0, max_requests - recent_requests)
        
        if is_allowed:
            # Add new request to bucket
            bucket[client_id].append((current_time, 1))
        
        return is_allowed, remaining
    
    async def __call__(self, request: Request) -> Optional[JSONResponse]:
        """Rate limit check for incoming request.
        
        Args:
            request: FastAPI request object
            
        Returns:
            None if allowed, JSONResponse with 429 if rate limited
        """
        client_id = self._get_client_id(request)
        
        # Clean old entries periodically
        self._clean_old_entries(self._minute_buckets, 60)
        self._clean_old_entries(self._hour_buckets, 3600)
        
        # Check minute limit
        minute_allowed, minute_remaining = self._check_limit(
            client_id,
            self._minute_buckets,
            self.requests_per_minute,
            60
        )
        
        if not minute_allowed:
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Maximum {self.requests_per_minute} requests per minute allowed",
                    "retry_after": 60
                },
                headers={
                    "Retry-After": "60",
                    "X-RateLimit-Limit": str(self.requests_per_minute),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(time.time() + 60))
                }
            )
        
        # Check hour limit
        hour_allowed, hour_remaining = self._check_limit(
            client_id,
            self._hour_buckets,
            self.requests_per_hour,
            3600
        )
        
        if not hour_allowed:
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Maximum {self.requests_per_hour} requests per hour allowed",
                    "retry_after": 3600
                },
                headers={
                    "Retry-After": "3600",
                    "X-RateLimit-Limit": str(self.requests_per_hour),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(time.time() + 3600))
                }
            )
        
        # Add rate limit headers to request state for response middleware
        request.state.rate_limit_remaining_minute = minute_remaining
        request.state.rate_limit_remaining_hour = hour_remaining
        
        return None


# Global rate limiter instance
rate_limiter = RateLimiter()


async def rate_limit_middleware(request: Request, call_next):
    """Middleware function for rate limiting.
    
    Args:
        request: FastAPI request object
        call_next: Next middleware/endpoint to call
        
    Returns:
        Response from next middleware/endpoint or rate limit response
    """
    # Check rate limit
    rate_limit_response = await rate_limiter(request)
    
    if rate_limit_response:
        return rate_limit_response
    
    # Continue to next middleware/endpoint
    response = await call_next(request)
    
    # Add rate limit headers to response
    if hasattr(request.state, "rate_limit_remaining_minute"):
        response.headers["X-RateLimit-Limit-Minute"] = str(rate_limiter.requests_per_minute)
        response.headers["X-RateLimit-Remaining-Minute"] = str(
            request.state.rate_limit_remaining_minute
        )
    
    if hasattr(request.state, "rate_limit_remaining_hour"):
        response.headers["X-RateLimit-Limit-Hour"] = str(rate_limiter.requests_per_hour)
        response.headers["X-RateLimit-Remaining-Hour"] = str(
            request.state.rate_limit_remaining_hour
        )
    
    return response
