from fastapi import FastAPI
from app.schemas.response import ResponseError, ResponseSuccess
# from app.core.logger import logger  # Assuming logger exists and is configured
# from app.api.v1.endpoints.user import router as user_router
from app.api.v1.endpoints.auth import router as auth_router
from datetime import datetime
from fastapi.responses import JSONResponse
from app.utils.response_helper import ResponseHelper
app = FastAPI(
    responses={
        400: {
            "model": ResponseError,
            "description": "Bad Request"
        },
        401: {
            "model": ResponseError,
            "description": "Credentials Invalid"
        },
        403: {
            "model": ResponseError,
            "description": "Forbidden"
        },
        422: {
            "model": ResponseError,
            "description": "Validation Error"
        },
        500: {
            "model": ResponseError,
            "description": "Internal Server Error"
        }
    }
)

# Include user and auth routes
# app.include_router(user_router, prefix="/api/v1/users", tags=["users"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])

@app.get("/", response_model=ResponseSuccess)
async def root():
   return ResponseHelper.status(203).json({
        "message": "Welcome to the User API!",
        "timestamp": datetime.now(),
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )
