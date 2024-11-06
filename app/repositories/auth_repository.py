from typing import Optional, Union
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.user import User
from bson import ObjectId
from app.models.auth import EmailAuthentication, GoogleAuthentication, Provider, Authentication
from app.core.exception import BadRequestException
from app.repositories.user_repository import UserRepository
from app.core.config import Logger
from datetime import datetime


class AuthRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.logger = Logger(__name__).get_logger()
        self.db = db
        self.user_repository = UserRepository(db)
        
    async def get_authentication_by_user_id(self, user_id: ObjectId) -> Optional[Authentication]:
        self.logger.debug(f"Fetching authentication by user ID: {user_id}")
        authentication = await self.db['authentications'].find_one({"user_id": user_id})
        return Authentication(**authentication) if authentication else None
    
    async def get_email_authentication_by_user_id(self, user_id: ObjectId) -> Optional[EmailAuthentication]:
        self.logger.debug(f"Fetching email authentication by user ID: {user_id}")
        email_authentication = await self.db['email_authentications'].find_one({"user_id": user_id})
        return EmailAuthentication(**email_authentication) if email_authentication else None
    
    async def get_google_authentication_by_user_id(self, user_id: ObjectId) -> Optional[GoogleAuthentication]:
        self.logger.debug(f"Fetching Google authentication by user ID: {user_id}")
        google_authentication = await self.db['google_authentications'].find_one({"user_id": user_id})
        return GoogleAuthentication(**google_authentication) if google_authentication else None               

    async def create_user(self, user: User, provider: Union[EmailAuthentication, GoogleAuthentication]) -> User:
        async def rollback():
            self.logger.debug(f"Rolling back user creation for user ID: {user.user_id}")
            # await self.db['users'].delete_one({"user_id": user.user_id})
            await self.db['authentications'].delete_one({"user_id": user.user_id})
            await self.user_repository.delete_user(user.user_id)
            if isinstance(provider, EmailAuthentication):
                await self.db['email_authentications'].delete_one({"user_id": user.user_id})
            elif isinstance(provider, GoogleAuthentication):
                await self.db['google_authentications'].delete_one({"user_id": user.user_id})

        try:
            self.logger.debug(f"Attempting to create user: {user.email}")
            if await self.user_repository.get_user_by_email(user.email):
                self.logger.error(f"User with email already exists: {user.email}")
                raise BadRequestException("User with email already exists")
            if isinstance(provider, GoogleAuthentication) and await self.get_user_by_google_id(provider.google_id):
                self.logger.error(f"User with Google ID already exists: {provider.google_id}")
                raise BadRequestException("User with Google ID already exists")
            
            authentication = Authentication(
                authentication_id=ObjectId(),
                provider=Provider.EMAIL if isinstance(provider, EmailAuthentication) else Provider.GOOGLE,
                user_id=user.user_id
            )
            
            await self.user_repository.create_user(user)
            await self.db['authentications'].insert_one(authentication.model_dump())
            
            if isinstance(provider, EmailAuthentication):
                await self.db['email_authentications'].insert_one(provider.model_dump())
            elif isinstance(provider, GoogleAuthentication):
                await self.db['google_authentications'].insert_one(provider.model_dump())
                
            self.logger.info(f"User created successfully: {user.email}")
            return user
        except BadRequestException as e:
            await rollback()
            self.logger.exception("BadRequestException occurred")
            raise e
        except Exception as e:
            await rollback()
            self.logger.exception("Unexpected error occurred while creating user")
            raise BadRequestException("Failed to create user due to an unexpected error") from e
    
    async def mark_email_as_verified(self, email: str) -> bool:
        self.logger.debug(f"Verifying email: {email}")
        
        mail = await self.db['email_authentications'].find_one_and_update(
            {"email": email},
            {"$set": {"email_verified_at": datetime.now()}}
        )
        if mail:
            self.logger.info(f"Email verified successfully: {email}")
            return True
        else:
            self.logger.warning(f"Email verification failed: {email}")
            return False
