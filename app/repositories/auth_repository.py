from typing import Optional, Union
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.user import User
from bson import ObjectId
from app.models.auth import EmailAuthentication, GoogleAuthentication, Provider, Authentication
from app.core.exception import BadRequestException
from app.core.config import Logger


class AuthRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.logger = Logger(__name__).get_logger()
        self.db = db

    async def get_user_by_email(self, email: str) -> Optional[User]:
        self.logger.debug(f"Fetching user by email: {email}")
        user = await self.db['users'].find_one({"email": email})
        if user:
            self.logger.info(f"User found: {user}")
        else:
            self.logger.warning(f"No user found with email: {email}")
        return User(**user) if user else None

    async def get_user_by_google_id(self, google_id: str) -> Optional[User]:
        self.logger.debug(f"Fetching user by Google ID: {google_id}")
        user = await self.db['users'].find_one({"google_id": google_id})
        if user:
            self.logger.info(f"User found: {user}")
        else:
            self.logger.warning(f"No user found with Google ID: {google_id}")
        return User(**user) if user else None

    async def get_user_by_id(self, user_id: ObjectId) -> Optional[User]:
        self.logger.debug(f"Fetching user by ID: {user_id}")
        user = await self.db['users'].find_one({"user_id": user_id})
        if user:
            self.logger.info(f"User found: {user}")
        else:
            self.logger.warning(f"No user found with ID: {user_id}")
        return User(**user) if user else None
    
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
            await self.db['users'].delete_one({"user_id": user.user_id})
            await self.db['authentications'].delete_one({"user_id": user.user_id})
            if isinstance(provider, EmailAuthentication):
                await self.db['email_authentications'].delete_one({"user_id": user.user_id})
            elif isinstance(provider, GoogleAuthentication):
                await self.db['google_authentications'].delete_one({"user_id": user.user_id})

        try:
            self.logger.debug(f"Attempting to create user: {user.email}")
            if await self.get_user_by_email(user.email):
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
            
            await self.db['users'].insert_one(user.model_dump())
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
