from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.schemas.response import ResponseError, ResponseModel
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.location import router as location_router
from fastapi.exceptions import RequestValidationError, HTTPException
from app.utils.get_error_details import get_error_details
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from app.core.middleware import (LoggingMiddleware, AuthenticationMiddleware, RoutingMiddleware)
from starlette.exceptions import HTTPException as StarletteHTTPException


app = FastAPI(
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
        404: {
            "model": ResponseModel,
            "description": "Not Found"
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
    msg = exc.errors()[0]['msg']
    return JSONResponse(
        status_code=422,
        content=ResponseError(
            message=f"Validation Error: {msg.split(',')[1].strip()}",
            errors=get_error_details(exc)
        ).model_dump()
    )
    
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ResponseModel(
            message=exc.detail
        ).model_dump()
    )
    
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, (
        HTTPException,
    )):
        return JSONResponse(
            status_code=exc.status_code,
            content=ResponseModel(
                message=exc.detail
            ).model_dump()
        )
        
    return JSONResponse(
        status_code=500,
        content=ResponseModel(
            message="Internal Server Error"
        ).model_dump()
    )

# Include user and auth routes
app.include_router(auth_router, prefix=settings.API_V1 + "auth", tags=["Authentication"])
app.include_router(location_router, prefix=settings.API_V1 + "location", tags=["Location"])

@app.get("/", response_model=ResponseModel)
async def root():
    return JSONResponse(
        status_code=200,
        content=ResponseModel(
            message="Welcome to the User API!"
        ).model_dump()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host=settings.APP_HOST, 
        port=settings.APP_PORT,
        reload=True
    )
