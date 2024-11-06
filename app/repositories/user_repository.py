from typing import Optional, Union
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.user import User
from bson import ObjectId
from app.core.exception import BadRequestException
from app.core.config import Logger


class UserRepository:
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
    
    async def create_user(self, user: User) -> User:
        self.logger.debug(f"Creating user: {user.email}")
        if await self.get_user_by_email(user.email):
            self.logger.error(f"User with email already exists: {user.email}")
            raise BadRequestException("User with email already exists")
        await self.db['users'].insert_one(user.model_dump())
        self.logger.info(f"User created successfully: {user.email}")
        return user
    
    async def update_user(self, user: User) -> User:
        self.logger.debug(f"Updating user: {user.email}")
        await self.db['users'].update_one({"user_id": user.user_id}, {"$set": user.model_dump()})
        self.logger.info(f"User updated successfully: {user.email}")
        return user
    
    async def delete_user(self, user_id: ObjectId) -> bool:
        self.logger.debug(f"Deleting user by ID: {user_id}")
        result = await self.db['users'].delete_one({"user_id": user_id})
        self.logger.info(f"User deleted successfully: {user_id}")
        return result.deleted_count > 0
    