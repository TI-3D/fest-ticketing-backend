import random
import hashlib
from datetime import datetime, timedelta
from app.schemas.otp import SendOtpRequest, SendOtpResponse, VerifyOtpRequest
from app.schemas.response import ResponseModel
from app.models.otp import OTP
from app.core.exception import BadRequestException, NotFoundException
from app.repositories.otp_repository import OtpRepository
from app.repositories.user_repository import UserRepository
from app.repositories.auth_repository import AuthRepository
from app.core.config import settings
import smtplib
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader

class MailService:
    def __init__(self, db):
        self.db = db
        self.otp_repository = OtpRepository(db)
        self.user_repository = UserRepository(db)
        self.auth_repository = AuthRepository(db)
        self.logger = Logger(__name__).get_logger()  # Initialize the logger

    async def send_otp(self, request: SendOtpRequest, ip_address) -> SendOtpResponse:
        self.logger.info(f"Attempting to send OTP to email: {request.email}, IP: {ip_address}")
        try:
            # Fetch the user by email
            user = await self.user_repository.get_user_by_email(request.email)
            if not user:
                self.logger.warning(f"Email {request.email} does not exist in the system.")
                raise BadRequestException("Email does not exist in the system.")
            
            # Generate OTP
            otp = str(random.randint(100000, 999999))
            expiration_time = datetime.now() + timedelta(minutes=5)  # OTP valid for 5 minutes
            
            # Hash the OTP to generate the unique hash
            combined_otp = f"{request.email}-{otp}"
            otp_hash = hashlib.sha256(combined_otp.encode()).hexdigest()

            # Create OTP document
            otp_details = OTP(
                email=request.email,
                otp=otp,  # Store the plain OTP in the database
                hash=otp_hash,
                expiration=expiration_time
            )

            # Save OTP details in the repository
            await self.otp_repository.save_otp(otp_details)
            self.logger.info(f"OTP for {request.email} generated and saved.")

            # Send OTP email
            self.send_email(user.full_name, request.email, otp, expiration_time, ip_address)
            self.logger.info(f"OTP email sent to {request.email}.")

            # Return the response
            return SendOtpResponse(
                message="OTP sent successfully",
                data={
                    "email": request.email,
                    "expiration": expiration_time,
                    "verification_hash": otp_hash
                }
            )
        except BadRequestException as e:
            self.logger.error(f"BadRequestException: {e}")
            raise e
        except Exception as e:
            self.logger.error(f"Failed to send OTP to {request.email}: {str(e)}")
            raise BadRequestException(f"Failed to send OTP: {str(e)}")

    async def verify_otp_with_hash(self, request: VerifyOtpRequest) -> ResponseModel:
        self.logger.info(f"Verifying OTP for hash: {request.hash}")
        try:
            # Retrieve OTP details by hash
            otp_details = await self.otp_repository.get_otp_by_hash(request.hash)

            if not otp_details:
                self.logger.warning(f"OTP not found or expired for hash: {request.hash}")
                raise BadRequestException("OTP has expired or was never sent.")

            # Check if OTP has expired
            if datetime.now() > otp_details.expiration:
                self.logger.warning(f"OTP expired for email: {otp_details.email}.")
                raise BadRequestException("OTP has expired.")

            # Verify OTP hash
            if request.hash != otp_details.hash:
                self.logger.warning(f"Invalid OTP hash for email: {otp_details.email}")
                raise BadRequestException("Invalid OTP hash.")
            
            # Delete the OTP after successful verification
            await self.otp_repository.delete_otp(otp_details.email)
            self.logger.info(f"OTP for email {otp_details.email} deleted after successful verification.")
            
            # Mark the user's email as verified
            await self.auth_repository.mark_email_as_verified(otp_details.email)
            self.logger.info(f"Email {otp_details.email} marked as verified.")

            return ResponseModel(message="Email verified successfully")
        except BadRequestException as e:
            self.logger.error(f"BadRequestException: {e}")
            raise e
        except Exception as e:
            self.logger.error(f"Failed to verify OTP for hash {request.hash}: {str(e)}")
            raise e

    async def resend_otp(self, request: SendOtpRequest, ip_address: str) -> SendOtpResponse:
        self.logger.info(f"Resending OTP to email: {request.email}, IP: {ip_address}")
        try:
            # Check if an active OTP exists for the user
            user = await self.user_repository.get_user_by_email(request.email)
            if not user:
                self.logger.warning(f"Email {request.email} does not exist in the system.")
                raise BadRequestException("Email does not exist in the system.")
            
            # Delete existing OTP
            await self.otp_repository.delete_otp(request.email)
            self.logger.info(f"Existing OTP for email {request.email} deleted.")

            # Generate OTP and send it again
            return await self.send_otp(request, ip_address)
        except BadRequestException as e:
            self.logger.error(f"BadRequestException: {e}")
            raise e
        except Exception as e:
            self.logger.error(f"Failed to resend OTP to {request.email}: {str(e)}")
            raise BadRequestException(f"Failed to resend OTP: {str(e)}")

    def send_email(self, name: str, email: str, otp: str, expiration_time: datetime, ip_address: str):
        self.logger.info(f"Sending OTP email to {email} from IP address {ip_address}.")
        # Setup email content
        template_env = Environment(loader=FileSystemLoader('templates'))
        template = template_env.get_template('otp_email_template.html')

        email_body = template.render(
            name=name,
            otp=otp,  # Send plain OTP in the email body
            expiration_time=expiration_time.strftime("%Y-%m-%d %H:%M:%S UTC"),
            ip_address=ip_address,
            company_name=settings.APP_NAME,
        )

        # SMTP setup and sending the email
        try:
            msg = EmailMessage()
            msg['Subject'] = "Your OTP Code"
            msg['From'] = settings.EMAILS_FROM_EMAIL
            msg['To'] = email
            msg.set_content("This email requires HTML support.")  # Fallback content for non-HTML email clients
            msg.add_alternative(email_body, subtype='html')

            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)

            self.logger.info(f"OTP email sent to {email} successfully.")
        except Exception as e:
            self.logger.error(f"Failed to send OTP email to {email}: {str(e)}")
            raise BadRequestException(f"Failed to send OTP email: {str(e)}")
