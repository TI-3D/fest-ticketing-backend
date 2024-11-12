from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import PersonalAccessToken, User
from app.core.config import Logger
from sqlalchemy import delete
from typing import Optional

class PersonalAccessTokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = Logger(__name__).get_logger()  # Initialize the logger

    async def get_token_by_id(self, token_id: int) -> Optional[PersonalAccessToken]:
        try:
            self.logger.info(f"Attempting to retrieve token by id: {token_id}")
            result = await self.session.execute(select(PersonalAccessToken).where(PersonalAccessToken.token_id == token_id))
            token = result.scalars().first()
            if not token:
                self.logger.warning(f"Token not found with id: {token_id}")
                raise HTTPException(status_code=404, detail=f"Token not found with id: {token_id}")
            self.logger.info(f"Token found with id: {token_id}")
            return token
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            raise 

    async def get_token_by_user_id(self, user_id: int) -> Optional[PersonalAccessToken]:
        try:
            self.logger.info(f"Attempting to retrieve token by user_id: {user_id}")
            result = await self.session.execute(select(PersonalAccessToken).where(PersonalAccessToken.user_id == user_id))
            token = result.scalars().first()
            if not token:
                self.logger.warning(f"Token not found for user_id: {user_id}")
                return None
            self.logger.info(f"Token found for user_id: {user_id}")
            return token
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            raise
    
    async def get_token_by_token(self, access_token: str) -> Optional[PersonalAccessToken]:
        try:
            self.logger.info(f"Attempting to retrieve token by token: {access_token}")
            result = await self.session.execute(select(PersonalAccessToken).where(PersonalAccessToken.access_token == access_token))
            access_token = result.scalars().first()
            if not access_token:
                self.logger.warning(f"Token not found with token: {access_token}")
                raise HTTPException(status_code=401, detail=f"Invalid credentials")
            self.logger.info(f"Token found with token: {access_token}")
            return access_token
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            raise
            
    async def create_token(self, token: PersonalAccessToken) -> PersonalAccessToken:
        try:
            self.logger.info(f"Attempting to create personal access token for user_id: {token.user_id}")
            self.session.add(token)  # Add the token object to the session
            self.logger.info(f"Personal access token for user_id {token.user_id} created successfully.")
            return token
        except Exception as e:
            self.logger.error(f"Error creating token: {str(e)}")
            raise 

    async def delete_token(self, token_id: int) -> bool:
        try:
            self.logger.info(f"Attempting to delete token with id: {token_id}")
            stmt = delete(PersonalAccessToken).where(PersonalAccessToken.token_id == token_id)
            result = await self.session.execute(stmt)
            if result.rowcount == 0:
                self.logger.warning(f"Token with id {token_id} not found for deletion.")
                raise HTTPException(status_code=404, detail=f"Token with id {token_id} not found for deletion")
            self.logger.info(f"Token with id {token_id} deleted successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Unexpected error deleting token: {str(e)}")
            raise 
