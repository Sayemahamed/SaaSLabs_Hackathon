import logging
import time

from prometheus_client import Counter, Histogram, start_http_server
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("api.middleware")

# Define Prometheus metrics
REQUEST_COUNTER = Counter(
    "http_requests_total", "Total number of HTTP requests", ["method", "path", "status"]
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "Latency of HTTP requests in seconds",
    ["method", "path", "status"],
)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        # Update Prometheus metrics
        REQUEST_COUNTER.labels(
            method=request.method, path=request.url.path, status=response.status_code
        ).inc()
        REQUEST_LATENCY.labels(
            method=request.method, path=request.url.path, status=response.status_code
        ).observe(process_time)

        # Log request details
        logger.info(
            f"{request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.4f}s"
        )
        return response


# Start Prometheus metric server on a specific port (e.g., 8001)
start_http_server(8001)
