from fastapi import APIRouter, Depends, Response, Request, HTTPException
from app.schemas.auth import SignupRequest, SigninRequest, SigninResponse, SignupResponse
from app.schemas.otp import VerifyOtpRequest, VerifyOtpResponse, SendOtpRequest, SendOtpResponse
from app.services.auth_service import AuthService
from app.dependencies.auth import get_access_token, get_current_user
from app.dependencies.database import get_db
from app.core.config import Logger
from app.schemas.response import ResponseModel, ResponseSuccess
from typing import Dict

router = APIRouter()
logger = Logger(__name__).get_logger()

@router.post("/signup", response_model=SignupResponse, status_code=201)
async def signup(
    request: SignupRequest,
    client: Request = None,
    db=Depends(get_db)
):
    auth_service = AuthService(db)
    client_ip = client.client.host if client else None  # Handle case if client is None
    logger.debug(f"Received signup request for email: {request.email}")
    
    try:
        signup_response = await auth_service.signup(request, client_ip)
        logger.info(f"User signed up successfully: {request.email}")
        return signup_response.model_dump()
    except HTTPException as e:
        logger.warning(f"Signup failed for {request.email}: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=str(e.detail))
    except Exception as e:
        logger.error(f"Unexpected error during signup for {request.email}: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@router.post("/verification", status_code=200)
async def verification(
    request: VerifyOtpRequest,
    db=Depends(get_db)
):
    auth_service = AuthService(db)
    logger.debug(f"Received verify request for email: {request.email}")

    try:
        verify_response = await auth_service.verify(request)
        logger.info(f"User verified successfully: {request.email}")
        return verify_response.model_dump()
    except HTTPException as e:
        logger.warning(f"Verification failed for {request.email}: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=str(e.detail))
    except Exception as e:
        logger.error(f"Unexpected error during verification for {request.email}: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
    
@router.post("/send-otp", response_model=SendOtpResponse)
async def send_otp(
    request: SendOtpRequest,
    client: Request = None,
    db=Depends(get_db)
):
    auth_service = AuthService(db)
    logger.debug(f"Received send OTP request for email: {request.email}")
    client_ip = client.client.host if client else None  # Handle case if client is None
    try:
        send_otp_response = await auth_service.send_otp(request, client_ip)
        logger.info(f"OTP sent successfully: {request.email}")
        return send_otp_response.model_dump()
    except HTTPException as e:
        logger.warning(f"Failed to send OTP for {request.email}: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=str(e.detail))
    except Exception as e:
        logger.error(f"Unexpected error during OTP send for {request.email}: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@router.post("/signin", response_model=SigninResponse)
async def signin(
    request: SigninRequest,
    db=Depends(get_db),
):
    auth_service = AuthService(db)
    logger.debug(f"Received signin request for email: {request.email}")
    
    try:
        signin_response = await auth_service.signin(request, False)
        logger.info(f"User signed in successfully: {request.email}")
        return signin_response.model_dump()
    except HTTPException as e:
        logger.warning(f"Signin failed for {request.email}: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=str(e.detail))
    except Exception as e:
        print(e)
        logger.error(f"Unexpected error during signin for {request.email}: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
    
@router.post("/admin/signin", response_model=SigninResponse)
async def signin(
    request: SigninRequest,
    db=Depends(get_db),
):
    auth_service = AuthService(db)
    logger.debug(f"Received signin request for email: {request.email}")
    
    try:
        signin_response = await auth_service.signin(request, True) 
        logger.info(f"User signed in successfully: {request.email}")
        return signin_response.model_dump()
    except HTTPException as e:
        logger.warning(f"Signin failed for {request.email}: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=str(e.detail))
    except Exception as e:
        print(e)
        logger.error(f"Unexpected error during signin for {request.email}: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
    
@router.get("/current", response_model=ResponseSuccess)
async def current_user(
    db=Depends(get_db),
    current_user: Dict = Depends(get_current_user),
):
    auth_service = AuthService(db)
    logger.debug(f"Received current user request for user ID: {current_user.get('sub')}")
    
    try:
        response = await auth_service.get_current_user(current_user.get('sub'))
        logger.info(f"Current user retrieved successfully: {current_user.get('sub')}")
        return response.model_dump()        
    except HTTPException as e:
        logger.warning(f"Unauthorized current user request: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=str(e.detail))
    except Exception as e:
        logger.error(f"Unexpected error during current user request: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
    
@router.delete("/signout", response_model=ResponseSuccess)
async def signout(
    db=Depends(get_db),
    access_token= Depends(get_access_token),
):
    auth_service = AuthService(db)
    logger.debug(f"Received logout request for access token: {access_token}")
    
    try:
        signout_response = await auth_service.signout(access_token)
        logger.info("User logged out successfully.")
        return signout_response.model_dump()
    except HTTPException as e:
        logger.warning(f"Unauthorized logout attempt: {str(e)}")
        raise HTTPException(status_code=e.status_code, detail=str(e.detail))
    except Exception as e:
        logger.error(f"Unexpected error during logout: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
