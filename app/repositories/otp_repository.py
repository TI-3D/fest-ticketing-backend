from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import OTP
from app.core.config import Logger
from sqlalchemy import delete
from typing import Optional
from datetime import datetime, timezone

class OTPRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = Logger(__name__).get_logger()  # Initialize the logger
        
    async def upsert(self, otp: OTP) -> OTP:
        """Insert or update an OTP record."""
        try:
            self.logger.info(f"Attempting to upsert OTP for user_id: {otp.user_id}")

            # Check if OTP already exists for the user_id
            existing_otp = await self.session.execute(select(OTP).where(OTP.user_id == otp.user_id))
            existing_otp = existing_otp.scalars().first()

            if existing_otp:
                self.logger.info(f"Updating OTP for user_id: {otp.user_id}")
                existing_otp.otp_code = otp.otp_code
                existing_otp.hashed_otp = otp.hashed_otp
                existing_otp.created_at = otp.created_at
                existing_otp.expires_in = otp.expires_in  # Make sure expires_in is updated
            else:
                # If OTP does not exist, create a new record
                self.logger.info(f"Creating new OTP for user_id: {otp.user_id}")
                self.session.add(otp)

            # Commit the session to persist changes
            await self.session.commit()

            # Return the OTP object after upsert
            self.logger.info(f"OTP for user_id {otp.user_id} upserted successfully.")
            return otp
        except Exception as e:
            self.logger.error(f"Unexpected error during upsert: {str(e)}")
            await self.session.rollback()
            raise
        
    async def get_otp_by_user_id(self, user_id: int) -> Optional[OTP]:
        """Retrieve OTP by user_id."""
        self.logger.info(f"Attempting to get OTP by user_id: {user_id}")
        result = await self.session.execute(select(OTP).where(OTP.user_id == user_id))
        return result.scalars().first()
        
        
    async def get_otp_by_hashed_otp(self, hashed_otp: str) -> Optional[OTP]:
        """Retrieve OTP by hashed value."""
        self.logger.info(f"Attempting to get OTP by hashed_otp: {hashed_otp}")
        result = await self.session.execute(select(OTP).where(OTP.hashed_otp == hashed_otp))
        return result.scalars().first()
    
    
    async def delete_expired_otps(self) -> bool:
        try:
            self.logger.info("Attempting to delete expired OTPs")
            stmt = delete(OTP).where((OTP.created_at + OTP.expires_in) < datetime.now(timezone.utc))
            result = await self.session.execute(stmt)
            await self.session.commit()
            self.logger.info(f"Deleted {result.rowcount} expired OTPs")
            return True
        except Exception as e:
            self.logger.error(f"Unexpected error deleting expired OTPs: {str(e)}")
            await self.session.rollback()
            raise
        
    async def delete_user_otps(self, user_id: int) -> bool:
        """Deletes OTPs for a given user."""
        try:
            self.logger.info(f"Attempting to delete OTPs for user_id: {user_id}")
            stmt = delete(OTP).where(OTP.user_id == user_id)
            result = await self.session.execute(stmt)
            await self.session.commit()
            self.logger.info(f"Deleted {result.rowcount} OTPs for user_id: {user_id}")
            return True
        except Exception as e:
            self.logger.error(f"Unexpected error deleting OTPs for user_id: {user_id}: {str(e)}")
            await self.session.rollback()
            raise
