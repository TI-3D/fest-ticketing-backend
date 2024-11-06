# app/api/v1/endpoints/mail.py
from fastapi import APIRouter, Depends, Request
from app.schemas.otp import SendOtpRequest, SendOtpResponse, VerifyOtpRequest
from app.schemas.response import ResponseModel
from app.dependencies import get_mongo_db
from app.services.mail_service import MailService
from app.core.config import Logger
from app.utils.response_helper import ResponseHelper
from app.core.exception import ServerErrorException, NotFoundException, BadRequestException

# Initialize the router and logger
router = APIRouter()
logger = Logger(__name__).get_logger()  # Initialize the logger

@router.post("/send-otp", response_model=SendOtpResponse)
async def send_otp(
    request: SendOtpRequest,
    db=Depends(get_mongo_db),
    client: Request = None
):
    client_ip = client.client.host  # Get client IP address
    mail_service = MailService(db)
    
    try:
        # Send OTP and include IP address in the process
        result = await mail_service.send_otp(request, client_ip)
        if not result:
            logger.error(f"Failed to send OTP to {request.email} from IP: {client_ip}")
            raise ServerErrorException("Failed to send OTP.")
        
        logger.info(f"OTP sent successfully to {request.email} from IP: {client_ip}")
        return ResponseHelper.status(200).json(result.model_dump())
    except NotFoundException as e:
        logger.error(f"Error while sending OTP to {request.email} from IP: {client_ip}: {str(e)}")
        raise e
    except BadRequestException as e:
        logger.error(f"Bad Request while sending OTP to {request.email} from IP: {client_ip}: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error while sending OTP to {request.email} from IP: {client_ip}: {str(e)}")
        raise ServerErrorException("Unexpected error while sending OTP")

@router.post("/verification", response_model=ResponseModel)
async def verify_otp(
    request: VerifyOtpRequest,
    db=Depends(get_mongo_db),
):
    mail_service = MailService(db)
    try:
        result = await mail_service.verify_otp_with_hash(request)
        return result
    except BadRequestException as e:
        logger.error(f"Bad Request while verifying OTP for {request.email}: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Error while verifying OTP for {request.email}: {str(e)}")
        raise ServerErrorException("Unexpected error while verifying OTP")
    

@router.post("/resend-otp", response_model=SendOtpResponse)
async def resend_otp(
    request: SendOtpRequest,
    db=Depends(get_mongo_db),
    client: Request = None
):
    client_ip = client.client.host  # Get client IP address
    mail_service = MailService(db)
    
    try:
        # Re Send OTP and include IP address in the process
        result = await mail_service.resend_otp(request, client_ip)
        if not result:
            logger.error(f"Failed to resend OTP to {request.email} from IP: {client_ip}")
            raise ServerErrorException("Failed to resend OTP.")
        
        logger.info(f"OTP sent successfully to {request.email} from IP: {client_ip}")
        return ResponseHelper.status(200).json(result.model_dump())
    except NotFoundException as e:
        logger.error(f"Error while sending OTP to {request.email} from IP: {client_ip}: {str(e)}")
        raise e
    except BadRequestException as e:
        logger.error(f"Bad Request while sending OTP to {request.email} from IP: {client_ip}: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error while sending OTP to {request.email} from IP: {client_ip}: {str(e)}")
        raise ServerErrorException("Unexpected error while sending OTP")

    

