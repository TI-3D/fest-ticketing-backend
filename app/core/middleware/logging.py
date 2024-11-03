from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response
from app.core.config import Logger

# Usage
logger = Logger(__name__).get_logger()

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host  # Get the client's IP address
        logger.info(f"Request from IP: {client_ip} - {request.method} {request.url}")
        logger.debug(f"Request headers: {request.headers}")  # Log request headers
        
        # Log the request body only if needed (be cautious with sensitive information)
        try:
            body = await request.body()
            logger.debug(f"Request body: {body.decode()}")  # Decode for better readability
        except Exception as e:
            logger.warning(f"Failed to log request body: {e}")

        response: Response = await call_next(request)

        logger.info(f"Response status: {response.status_code}")
        logger.debug(f"Response headers: {response.headers}")  # Log response headers

        return response