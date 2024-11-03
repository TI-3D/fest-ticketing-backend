from fastapi import APIRouter, Depends, Response
from app.schemas.auth import SignupRequest, SigninRequest, GoogleSigninRequest, SigninResponse, SignupResponse
from app.services.auth_service import AuthService
from app.dependencies import get_mongo_db, get_access_token
from app.utils.response_helper import ResponseHelper, Cookie
from app.core.config import settings
from app.schemas.response import ResponseModel
from app.core.exception import (NotFoundException, BadRequestException, UnauthorizedException, ServerErrorException)
from app.core.config import Logger

router = APIRouter()
logger = Logger(__name__).get_logger()  # Initialize the logger


@router.post("/signup", response_model=SignupResponse)
async def signup(
    request: SignupRequest,
    db=Depends(get_mongo_db)
):
    auth_service = AuthService(db)
    logger.debug(f"Received signup request for email: {request.email}")
    try:
        signup_response = await auth_service.signup(request)
        logger.info(f"User signed up successfully: {request.email}")
        return ResponseHelper.status().json(signup_response.model_dump())
    except BadRequestException as e:
        logger.warning(f"Signup failed for {request.email}: {str(e)}")
        raise BadRequestException(str(e))
    except Exception as e:
        logger.error(f"Unexpected error during signup for {request.email}: {str(e)}")
        raise ServerErrorException("An unexpected error occurred")


@router.post("/signin", response_model=SigninResponse)
async def signin(
    request: SigninRequest,
    db=Depends(get_mongo_db)
):
    auth_service = AuthService(db)
    logger.debug(f"Received signin request for email: {request.email}")
    try:
        signin_response = await auth_service.signin(request)
        logger.info(f"User signed in successfully: {request.email}")
        return ResponseHelper.status().json(signin_response.model_dump())
    except NotFoundException as e:
        logger.warning(f"User not found during signin for {request.email}: {str(e)}")
        raise NotFoundException(str(e))
    except BadRequestException as e:
        logger.warning(f"Invalid credentials during signin for {request.email}: {str(e)}")
        raise BadRequestException(str(e))
    except Exception as e:
        logger.error(f"Unexpected error during signin for {request.email}: {str(e)}")
        raise ServerErrorException("An unexpected error occurred")


@router.post("/google-signin", response_model=SigninResponse)
async def google_signin(
    request: GoogleSigninRequest,
    db=Depends(get_mongo_db),
):
    auth_service = AuthService(db)
    logger.debug("Received Google signin request")
    try:
        google_signin_response = await auth_service.google_signin(request)
        logger.info(f"User signed in successfully with Google: {google_signin_response.data['user']['email']}")
        return ResponseHelper.json(google_signin_response.dict())
    except BadRequestException as e:
        logger.error(f"Invalid Google ID token: {str(e)}")
        raise BadRequestException(str(e))
    except Exception as e:
        logger.error(f"Unexpected error during Google signin: {str(e)}")
        raise ServerErrorException("An unexpected error occurred")


@router.post("/signout", response_model=ResponseModel)
async def signout(
    db=Depends(get_mongo_db),
    access_token= Depends(get_access_token),
):
    auth_service = AuthService(db)
    logger.debug(f"Received logout request for access token: {access_token}")
    try:
        await auth_service.signout(access_token)
        logger.info("User logged out successfully.")
        return ResponseHelper.status().json({
            "message": "User logged out successfully."
        })
    # except UnauthorizedException as e:
    #     logger.warning(f"Unauthorized logout attempt: {str(e)}")
    #     raise e
    except Exception as e:
        logger.error(f"Unexpected error during logout: {str(e)}")
        raise e
