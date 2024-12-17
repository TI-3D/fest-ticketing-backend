from app.repositories import OTPRepository, UserRepository
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
import random
from app.core.security import generate_otp_secret
from app.models.otp import OTP, VerificationType
from app.schemas.otp import VerifyOtpRequest
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.mail_service import MailService


class OTPService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.mail_service = MailService()
        self.user_repository = UserRepository(session)
        self.otp_repository = OTPRepository(session)

    def generate_otp(self, length: int = 6) -> str:
        """Generates a random OTP."""
        return str(random.randint(100000, 999999)).zfill(length)

    async def generate_and_save(self, user_id: str, token_type: VerificationType, client_ip:str) -> OTP:
        """Generates and saves an OTP for the user."""
        otp_code = self.generate_otp()
        secret = generate_otp_secret()  # Generate OTP secret
        expires_in = timedelta(minutes=5)  # Set expiration time, for example, 5 minutes
        user = await self.user_repository.get_user_by_id(user_id)
        otp = OTP(
            user_id=user_id,
            otp_code=otp_code,
            hashed_otp=secret,
            token_type=token_type,
            created_at=datetime.now(timezone.utc),
            expires_in=int(expires_in.total_seconds()),
        )
        expires_at = datetime.now(timezone.utc) + expires_in
        
        await self.otp_repository.upsert(otp)
        await self.mail_service.send_otp_email(user.full_name, user.email, otp.otp_code, expires_at, client_ip)
        return otp

    async def regenerate_otp(self, user_id: str, client_ip:str) -> OTP:
        """Regenerates the OTP for the given user."""
        otp = await self.otp_repository.get_otp_by_user_id(user_id)
        if not otp:
            raise HTTPException(status_code=400, detail="No OTP found for the user")
        otp_code = self.generate_otp()
        secret = generate_otp_secret()
        expires_in = timedelta(minutes=5)
        user = await self.user_repository.get_user_by_id(user_id)        
        otp.otp_code = otp_code
        otp.hashed_otp = secret
        otp.created_at = datetime.now(timezone.utc)
        otp.expires_in = int(expires_in.total_seconds())
        expires_at = datetime.now(timezone.utc) + expires_in
        await self.otp_repository.upsert(otp)
        await self.mail_service.send_otp_email(user.full_name, user.email, otp.otp_code, expires_at, client_ip)
        
        return otp

    async def verify_otp(self, request: VerifyOtpRequest) -> VerificationType:
        """Verifies the OTP for the given user."""
        otp = await self.otp_repository.get_otp_by_hashed_otp(request.hash)
        if not otp:
            raise HTTPException(status_code=400, detail="Invalid OTP")
        
        if otp.hashed_otp != request.hash or otp.otp_code != request.otp:
            raise HTTPException(status_code=400, detail="Invalid OTP")
        
        if otp.token_type == VerificationType.REGISTRATION:
            await self.user_repository.mark_email_verified(otp.user_id)
        token_type = otp.token_type
        await self.otp_repository.delete_user_otps(otp.user_id)
        return token_type
