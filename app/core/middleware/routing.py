from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.exception import NotFoundException
from app.core.config import Logger

logger = Logger(__name__).get_logger()

class RoutingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        logger.info(f"Response: {response.status_code}")
        if response.status_code == 404:
            logger.warning("Resource not found")
            raise NotFoundException("Resource not found")
        
        return response