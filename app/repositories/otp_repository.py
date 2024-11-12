from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import OTP
from app.core.config import Logger
from sqlalchemy import delete
from typing import Optional
from datetime import datetime

class OTPRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = Logger(__name__).get_logger()  # Initialize the logger
        
    async def upsert(self, otp: OTP) -> OTP:
        try:
            self.logger.info(f"Attempting to upsert OTP for user_id: {otp.user_id}")

            # Check if OTP already exists for the user_id
            result = await self.session.execute(select(OTP).where(OTP.user_id == otp.user_id))
            existing_otp = result.scalars().first()

            if existing_otp:
                # If OTP exists, update the existing record
                self.logger.info(f"Updating OTP for user_id: {otp.user_id}")
                existing_otp.otp_code = otp.otp_code
                existing_otp.hashed_otp = otp.hashed_otp
                existing_otp.created_at = otp.created_at
                existing_otp.expires_at = otp.expires_at
                # Optionally, update other fields here
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
        
    async def get_otp_by_code(self, otp_code: str) -> Optional[OTP]:
        try:
            self.logger.info(f"Attempting to retrieve OTP by code: {otp_code}")
            result = await self.session.execute(select(OTP).where(OTP.otp_code == otp_code))
            otp = result.scalars().first()
            if not otp:
                self.logger.warning(f"OTP not found with code: {otp_code}")
                return None  # Return None instead of raising an exception
            self.logger.info(f"OTP found with code: {otp_code}")
            return otp
        except Exception as e:
            self.logger.error(f"Error retrieving OTP by code: {str(e)}")
            raise
        
    async def get_otp_by_hashed_otp(self, hashed_otp: str) -> Optional[OTP]:
        try:
            self.logger.info(f"Attempting to retrieve OTP by hashed OTP: {hashed_otp}")
            result = await self.session.execute(select(OTP).where(OTP.hashed_otp == hashed_otp))
            otp = result.scalars().first()
            if not otp:
                self.logger.warning(f"OTP not found with hashed OTP: {hashed_otp}")
                return None  # Return None instead of raising an exception
            self.logger.info(f"OTP found with hashed OTP: {hashed_otp}")
            return otp
        except Exception as e:
            self.logger.error(f"Error retrieving OTP by hashed OTP: {str(e)}")
            raise    
    
    async def create(self, otp: OTP) -> OTP:
        try:
            self.logger.info(f"Attempting to create OTP for user_id: {otp.user_id}")
            self.session.add(otp)  # Add the OTP object to the session
            self.logger.info(f"OTP for user_id {otp.user_id} created successfully.")
            return otp
        except Exception as e:
            self.logger.error(f"Error creating OTP: {str(e)}")
            raise

    async def delete_expired_otps(self) -> bool:
        try:
            self.logger.info("Attempting to delete expired OTPs")
            stmt = delete(OTP).where(OTP.expires_at < datetime.now())
            result = await self.session.execute(stmt)
            self.logger.info(f"Deleted {result.rowcount} expired OTPs")
            return True
        except Exception as e:
            self.logger.error(f"Unexpected error deleting expired OTPs: {str(e)}")
            raise
        
    async def delete_user_otps(self, user_id: int) -> bool:
        try:
            self.logger.info(f"Attempting to delete OTPs for user_id: {user_id}")
            stmt = delete(OTP).where(OTP.user_id == user_id)
            result = await self.session.execute(stmt)
            self.logger.info(f"Deleted {result.rowcount} OTPs for user_id: {user_id}")
            return True
        except Exception as e:
            self.logger.error(f"Unexpected error deleting OTPs for user_id {user_id}: {str(e)}")
            raise
