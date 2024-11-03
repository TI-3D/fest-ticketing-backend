from typing import Optional
from datetime import datetime, timedelta
from pydantic import EmailStr
from app.models.personal_access_token import PersonalAccessToken
from app.models.user import User
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from app.core.exception import (
    NotFoundException,
    ServerErrorException,
    UnauthorizedException
)
from app.core.security import create_access_token, verify_access_token
from app.core.config import Logger


class PersonalAccessTokenRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        # Usage
        self.logger = Logger(__name__).get_logger()
        self.db = db

    async def create_token(self, user_id: ObjectId, email: EmailStr, device_id: Optional[str] = None, is_google: bool = False) -> PersonalAccessToken:
        try:
            access_token = create_access_token(user_id, email, is_google)
            token = PersonalAccessToken(
                personal_access_token_id=ObjectId(),
                user_id=user_id,
                device_id=device_id,
                access_token=access_token.token,
                access_token_expired=datetime.now() + timedelta(seconds=access_token.expires_in),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            await self.db["personal_access_tokens"].insert_one(token.model_dump())
            self.logger.info(f"Token created for user {user_id}.")
            return token
        except Exception as e:
            self.logger.error(f"Error creating token for user {user_id}: {e}")
            raise ServerErrorException("An error occurred while creating the token")

    async def get_user_by_access_token(self, access_token: str) -> Optional[User]:
        try:
            user_id = await verify_access_token(self.db, access_token)
            user = await self.db["users"].find_one({"user_id": user_id})
            self.logger.info(f"User retrieved for access token: {access_token}.")
            return User(**user) if user else None
        except UnauthorizedException as e:
            self.logger.warning(f"Unauthorized access attempt with token: {access_token}.")
            raise e
        except NotFoundException as e:
            self.logger.warning(f"User not found exception: {e}.")
            raise e
        except Exception as e:
            self.logger.error(f"Error retrieving user by access token: {e}.")
            raise ServerErrorException("An error occurred while getting the user")



    async def delete_token(self, access_token: str) -> bool:
        try:
            user_id = await verify_access_token(self.db, access_token)
            if not user_id:
                raise UnauthorizedException("Invalid credentials")
            await self.db["personal_access_tokens"].delete_one({"access_token": access_token})
            self.logger.info(f"Token deleted for user {user_id}.")
            return True
        except UnauthorizedException as e:
            self.logger.warning(f"Unauthorized access attempt with token: {access_token}.")
            raise e
        except Exception as e:
            self.logger.error(f"Error deleting token for user: {e}.")
            raise ServerErrorException("An error occurred while deleting the token")
