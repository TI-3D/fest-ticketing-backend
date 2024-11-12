from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from app.models import User
from app.core.config import Logger
from typing import Optional
from fastapi import HTTPException  # Import HTTPException from FastAPI

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = Logger(__name__).get_logger()  # Initialize the logger

    async def create(self, user: User) -> User:
        try:
            self.logger.info(f"Attempting to create user with email: {user.email}")
            self.session.add(user)  # Add the user object to the session
            await self.session.flush()  # Ensure the user_id is generated
            await self.session.refresh(user)  # Refresh to populate user_id
            self.logger.info(f"User with email {user.email} created successfully.")
            return user
        except Exception as e:
            self.logger.error(f"Error creating user with email {user.email}: {str(e)}")
            raise HTTPException(status_code=400, detail="Error creating user")

    async def get_user_by_email(self, email: str) -> Optional[User]:
        try:
            self.logger.info(f"Attempting to retrieve user by email: {email}")
            result = await self.session.execute(select(User).where(User.email == email))
            user = result.scalars().first()
            if not user:
                self.logger.warning(f"User not found with email: {email}")
                return None
            self.logger.info(f"User found with email: {email}")
            return user
        except Exception as e:
            self.logger.error(f"Error retrieving user by email {email}: {str(e)}")
            raise HTTPException(status_code=400, detail="Error retrieving user by email")

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        try:
            self.logger.info(f"Attempting to retrieve user by id: {user_id}")
            result = await self.session.execute(select(User).where(User.user_id == user_id))
            user = result.scalars().first()
            if not user:
                self.logger.warning(f"User not found with id: {user_id}")
                return None
            self.logger.info(f"User found with id: {user_id}")
            return user
        except Exception as e:
            self.logger.error(f"Error retrieving user by id {user_id}: {str(e)}")
            raise HTTPException(status_code=400, detail="Error retrieving user by id")

    async def update(self, user_id: int, updates: dict) -> User:
        try:
            self.logger.info(f"Attempting to update user with id: {user_id}")
            stmt = update(User).where(User.user_id == user_id).values(**updates)
            result = await self.session.execute(stmt)
            if result.rowcount == 0:
                self.logger.warning(f"User with id {user_id} not found for update.")
                raise HTTPException(status_code=400, detail=f"User with id {user_id} not found for update.")
            self.logger.info(f"User with id {user_id} updated successfully.")
            return await self.get_user_by_id(user_id)  # Return the updated user
        except Exception as e:
            self.logger.error(f"Unexpected error updating user with id {user_id}: {str(e)}")
            raise HTTPException(status_code=400, detail="Error updating user")

    async def delete(self, user_id: int) -> bool:
        try:
            self.logger.info(f"Attempting to delete user with id: {user_id}")
            stmt = delete(User).where(User.user_id == user_id)
            result = await self.session.execute(stmt)
            if result.rowcount == 0:
                self.logger.warning(f"User with id {user_id} not found for deletion.")
                raise HTTPException(status_code=400, detail=f"User with id {user_id} not found for deletion.")
            self.logger.info(f"User with id {user_id} deleted successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Unexpected error deleting user with id {user_id}: {str(e)}")
            raise HTTPException(status_code=400, detail="Error deleting user")
