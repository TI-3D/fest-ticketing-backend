from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from app.models import Provider
from app.core.config import Logger
from typing import Optional, List
from app.core.exception import BadRequestException
from app.models.provider import Provider, ProviderName

class ProviderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = Logger(__name__).get_logger()  # Initialize the logger

    async def create(self, provider: Provider) -> Provider:
        """
        Create a new provider record and associate it with a user.
        """
        try:
            self.logger.info(f"Attempting to create provider for user_id: {provider.user_id}, provider_name: {provider.provider_name}")
            self.session.add(provider)
            await self.session.flush()  # Ensure the provider_id is generated
            await self.session.refresh(provider)  # Refresh to populate provider_id
            self.logger.info(f"Provider created successfully for user_id: {provider.user_id}, provider_name: {provider.provider_name}")
            return provider
        except Exception as e:
            self.logger.error(f"Error creating provider for user_id: {provider.user_id}: {str(e)}")
            raise

    async def get_by_user_id(self, user_id: str) -> List[Provider]:
        """
        Get all providers associated with a given user_id.
        """
        try:
            self.logger.info(f"Attempting to retrieve providers for user_id: {user_id}")
            result = await self.session.execute(select(Provider).where(Provider.user_id == user_id))
            providers = result.scalars().all()
            if not providers:
                self.logger.warning(f"No providers found for user_id: {user_id}")
            else:
                self.logger.info(f"Found {len(providers)} providers for user_id: {user_id}")
            return providers
        except Exception as e:
            self.logger.error(f"Error retrieving providers for user_id {user_id}: {str(e)}")
            raise
    
    async def get_by_provider_name_by_user_id(self, user_id: str, provider_name: ProviderName = ProviderName.EMAIL ) -> Optional[Provider]:
        """
        Get a provider by provider name (e.g., Google, Facebook) and user_id.
        """
        try:
            self.logger.info(f"Attempting to retrieve provider for user_id: {user_id}, provider_name: {provider_name}")
            result = await self.session.execute(select(Provider).where(Provider.user_id == user_id, Provider.provider_name == provider_name))
            provider = result.scalars().first()
            if not provider:
                self.logger.warning(f"No provider found for user_id: {user_id}, provider_name: {provider_name}")
            else:
                self.logger.info(f"Found provider for user_id: {user_id}, provider_name: {provider_name}")
            return provider
        except Exception as e:
            self.logger.error(f"Error retrieving provider for user_id {user_id}, provider_name {provider_name}: {str(e)}")
            raise

    async def get_by_provider_name(self, provider_name: ProviderName) -> List[Provider]:
        """
        Get all providers by provider name (e.g., Google, Facebook).
        """
        try:
            self.logger.info(f"Attempting to retrieve providers for provider_name: {provider_name}")
            result = await self.session.execute(select(Provider).where(Provider.provider_name == provider_name))
            providers = result.scalars().all()
            if not providers:
                self.logger.warning(f"No providers found for provider_name: {provider_name}")
            else:
                self.logger.info(f"Found {len(providers)} providers for provider_name: {provider_name}")
            return providers
        except Exception as e:
            self.logger.error(f"Error retrieving providers for provider_name {provider_name}: {str(e)}")
            raise

    async def update(self, provider_id: int, updates: dict) -> Provider:
        """
        Update a provider's details by provider_id.
        """
        try:
            self.logger.info(f"Attempting to update provider with provider_id: {provider_id}")
            async with self.session.begin():
                stmt = update(Provider).where(Provider.provider_id == provider_id).values(**updates)
                result = await self.session.execute(stmt)
                if result.rowcount == 0:
                    self.logger.warning(f"Provider with id {provider_id} not found for update.")
                    raise BadRequestException(f"Provider with id {provider_id} not found.")
            self.logger.info(f"Provider with provider_id {provider_id} updated successfully.")
        except BadRequestException as e:
            self.logger.error(f"Error: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error updating provider with provider_id {provider_id}: {str(e)}")
            raise

    async def delete(self, provider_id: int) -> bool:
        """
        Delete a provider by provider_id.
        """
        try:
            self.logger.info(f"Attempting to delete provider with provider_id: {provider_id}")
            async with self.session.begin():
                stmt = delete(Provider).where(Provider.provider_id == provider_id)
                result = await self.session.execute(stmt)
                if result.rowcount == 0:
                    self.logger.warning(f"Provider with provider_id {provider_id} not found for deletion.")
                    raise BadRequestException(f"Provider with provider_id {provider_id} not found.")
            self.logger.info(f"Provider with provider_id {provider_id} deleted successfully.")
            return True
        except BadRequestException as e:
            self.logger.error(f"Error: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error deleting provider with provider_id {provider_id}: {str(e)}")
            raise
