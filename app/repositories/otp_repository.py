from pymongo import ReturnDocument
from app.models.otp import OTP
from app.core.exception import BadRequestException
from app.core.config import Logger

class OtpRepository:
    def __init__(self, db):
        self.db = db
        self.logger = Logger(__name__).get_logger()  # Initialize the logger
    
    async def save_otp(self, otp_details: OTP):
        # Log OTP save operation
        self.logger.info(f"Saving OTP for email: {otp_details.email}")
        try:
            result = await self.db["otps"].replace_one(
                {"email": otp_details.email}, otp_details.model_dump(), upsert=True
            )
            self.logger.info(f"OTP for email {otp_details.email} saved successfully.")
        except Exception as e:
            self.logger.error(f"Error saving OTP for email {otp_details.email}: {e}")
            raise
    
    async def get_otp_by_email(self, email: str) -> OTP:
        # Log OTP fetch operation
        self.logger.info(f"Fetching OTP for email: {email}")
        otp_data = await self.db["otps"].find_one({"email": email})
        if not otp_data:
            self.logger.warning(f"OTP not found or expired for email: {email}")
            raise BadRequestException("OTP has expired or was never sent.")
        self.logger.info(f"OTP fetched for email: {email}")
        return OTP(**otp_data)
    
    async def get_otp_by_hash(self, hash: str) -> OTP:
        # Log OTP fetch by hash operation
        self.logger.info(f"Fetching OTP for hash: {hash}")
        otp_data = await self.db["otps"].find_one({"hash": hash})
        if not otp_data:
            self.logger.warning(f"OTP not found or expired for hash: {hash}")
            raise BadRequestException("OTP has expired or was never sent.")
        self.logger.info(f"OTP fetched for hash: {hash}")
        return OTP(**otp_data)

    async def update_otp(self, email: str, otp_details: OTP) -> OTP:
        # Log OTP update operation
        self.logger.info(f"Updating OTP for email: {email}")
        try:
            updated_otp = await self.db["otps"].find_one_and_replace(
                {"email": email}, otp_details.model_dump(), return_document=ReturnDocument.AFTER
            )
            if not updated_otp:
                self.logger.warning(f"Failed to update OTP for email: {email}")
                raise BadRequestException("Failed to update OTP.")
            self.logger.info(f"OTP for email {email} updated successfully.")
            return OTP(**updated_otp)
        except Exception as e:
            self.logger.error(f"Error updating OTP for email {email}: {e}")
            raise
    
    async def delete_otp(self, email: str):
        # Log OTP delete operation
        self.logger.info(f"Deleting OTP for email: {email}")
        try:
            result = await self.db["otps"].delete_many({"email": email})
            if result.deleted_count > 0:
                self.logger.info(f"OTP for email {email} deleted successfully.")
            else:
                self.logger.warning(f"No OTP found for email {email} to delete.")
        except Exception as e:
            self.logger.error(f"Error deleting OTP for email {email}: {e}")
            raise
