from fastapi import HTTPException
from app.models.otp import OTP
from app.repositories import OTPRepository, UserRepository
from app.core.security import create_jwt_token, verify_jwt_token
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.services.mail_service import MailService
from datetime import datetime, timedelta, timezone
from app.schemas.otp import VerifyOtpRequest
import random

class OTPService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.mail_service = MailService()
        self.otp_repository = OTPRepository(session)
        self.user_repository = UserRepository(session)
    
    def generate_otp(self, length: int = 6) -> str:
        """Generates a random OTP."""
        return str(random.randint(100000, 999999)).zfill(length)

    async def generate_and_save(self, user_id: int, client_ip: str) -> OTP:
        """Generates and saves an OTP for the user."""
        try:
            user = await self.user_repository.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            await self.delete_expired_otps()  # Delete expired OTPs
            otp_code = self.generate_otp()  # Generate OTP
            expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)  # OTP expiration time
            hashed_otp = create_jwt_token({"user_id": user_id, "otp": otp_code}, expires_at=expires_at)  # Generate hashed OTP
            otp = OTP(user_id=user_id, otp_code=otp_code, hashed_otp=hashed_otp, created_at=datetime.now(timezone.utc), expires_at=expires_at)

            # No transaction handling here, let the service handle that
            await self.otp_repository.upsert(otp)
            await self.mail_service.send_otp_email(user.full_name, user.email, otp.otp_code, otp.expires_at, client_ip)
            return otp
        except SQLAlchemyError as e:
            raise Exception(f"Error generating OTP: {e}")
        

    async def verify_otp(self, request: VerifyOtpRequest) -> bool:
        """Verifies the OTP for the given user."""
        try:
            data = verify_jwt_token(request.hash)
            
            if not data:
                raise HTTPException(status_code=400, detail="Invalid OTP")
            
            otp = await self.otp_repository.get_otp_by_hashed_otp(request.hash)
            user_id = data.get("user_id")
            
            if not otp:
                raise HTTPException(status_code=400, detail="Invalid OTP")
            
            if otp.expires_at < datetime.now(timezone.utc):
                raise HTTPException(status_code=400, detail="OTP has expired")
            
            if otp.user_id != user_id:
                raise HTTPException(status_code=400, detail="Invalid OTP")
            
            if otp.otp_code == request.otp:
                print(otp)
                await self.otp_repository.delete_user_otps(user_id)
                return True
            else:
                raise HTTPException(status_code=400, detail="Invalid OTP")
        except SQLAlchemyError as e:
            raise Exception(f"Error verifying OTP: {e}")
        
    async def delete_expired_otps(self):
        """Deletes all expired OTPs."""
        try:
            await self.otp_repository.delete_expired_otps()
        except SQLAlchemyError as e:
            raise Exception(f"Error deleting expired OTPs: {e}")
    
    async def delete_user_otps(self, user_id: int):
        """Deletes all OTPs for the given user."""
        try:
            await self.otp_repository.delete_user_otps(user_id)
        except SQLAlchemyError as e:
            raise Exception(f"Error deleting user OTPs: {e}")