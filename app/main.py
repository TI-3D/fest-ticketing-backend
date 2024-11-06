from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from app.schemas.response import ResponseError, ResponseModel, ResponseSuccess, ErrorDetail
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.mail import router as mail_router
from datetime import datetime
from app.utils.response_helper import ResponseHelper
from fastapi.exceptions import RequestValidationError, HTTPException
from app.utils.get_error_details import get_error_details
from app.dependencies.database import init_db
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from app.core.middleware import (LoggingMiddleware, AuthenticationMiddleware, RoutingMiddleware)
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.exception import (
    UnauthorizedException,
    BadRequestException,
    ForbiddenException,
    NotFoundException,
    MethodNotAllowedException,
    ServerErrorException,
    RedirectionException    
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_db()
        yield
    finally:
        pass 
    
app = FastAPI(
    lifespan=lifespan,
    responses={
        400: {
            "model": ResponseModel,
            "description": "Bad Request"
        },
        401: {
            "model": ResponseModel,
            "description": "Credentials Invalid"
        },
        403: {
            "model": ResponseModel,
            "description": "Forbidden"
        },
        422: {
            "model": ResponseError,
            "description": "Validation Error"
        },
        500: {
            "model": ResponseModel,
            "description": "Internal Server Error"
        }
    }
)

# Setup middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RoutingMiddleware)
app.add_middleware(AuthenticationMiddleware)

# handle 422 error
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError | ValueError):
    return ResponseHelper.status(422).json({
        "message": "Validation Error",
        "errors": get_error_details(exc),
        
    })
    
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return ResponseHelper.status(exc.status_code).json({
        "message": exc.detail
    })

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    # Check for known HTTP exceptions
    if isinstance(exc, (
        HTTPException,
        NotFoundException,  
        UnauthorizedException, 
        MethodNotAllowedException,
        BadRequestException, 
        ForbiddenException, 
        ServerErrorException, 
        RedirectionException
    )):
        return ResponseHelper.status(exc.status_code).json({
            "message": exc.detail
        })
    # Fallback for any other exceptions
    return ResponseHelper.status(500).json({
        "message": "Internal Server Error",
    })


# Include user and auth routes
app.include_router(auth_router, prefix=settings.API_V1 + "auth", tags=["Authentication"])
app.include_router(mail_router, prefix=settings.API_V1 + "mail", tags=["Mail"])

@app.get("/", response_model=ResponseSuccess)
async def root():
   return ResponseHelper.status().json({
        "message": "Welcome to the User API!"
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host=settings.APP_HOST, 
        port=settings.APP_PORT,
        reload=True
    )
