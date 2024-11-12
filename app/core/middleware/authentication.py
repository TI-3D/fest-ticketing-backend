from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response, FastAPI
from app.core.exception import UnauthorizedException
from app.core.config import Logger, settings

# Usage
logger = Logger(__name__).get_logger()
class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Define paths that don't require authentication
        excluded_paths = settings.AUTH_EXCLUDED_PATHS
        
        # Check if the request path is in the excluded paths
        if request.url.path in excluded_paths:
            logger.debug(f"Guest access allowed for path: {request.url.path}")
            return await call_next(request)

        # Access the FastAPI app from the request
        app = request.app
        
        # Check if the request path is valid (exists in routes)
        if not any(route.path == request.url.path for route in app.routes):
            return await call_next(request)  # Pass to the NotFoundMiddleware
        
        # Check for token in the Authorization header
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            logger.warning("Unauthorized access attempt: No valid token provided.")
            raise UnauthorizedException("Invalid credentials")

        logger.info(f"Authenticated access for path: {request.url.path}")
        response: Response = await call_next(request)
        return response

