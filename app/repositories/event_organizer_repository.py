from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import List, Optional
from app.models import EventOrganizer, OrganizerStatus
from app.core.config import Logger


class EventOrganizerRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = Logger(__name__).get_logger()

    async def get_all_organizers(self) -> List[EventOrganizer]:
        """
        Retrieve all event organizers.
        """
        try:
            self.logger.info("Attempting to retrieve all event organizers")
            result = await self.session.execute(select(EventOrganizer))
            organizers = result.scalars().all()
            return organizers
        except Exception as e:
            self.logger.error(f"Error retrieving all event organizers: {str(e)}")
            raise

    async def get_organizer_by_id(self, organizer_id: str) -> Optional[EventOrganizer]:
        """
        Retrieve an event organizer by its ID.
        """
        try:
            self.logger.info(f"Retrieving event organizer with ID: {organizer_id}")
            result = await self.session.execute(
                select(EventOrganizer).filter(EventOrganizer.organizer_id == organizer_id)
            )
            organizer = result.scalars().first()
            return organizer
        except Exception as e:
            self.logger.error(f"Error retrieving organizer by ID {organizer_id}: {str(e)}")
            raise
        
    async def get_organizer_by_user_id(self, user_id: str) -> Optional[EventOrganizer]:
        """
        Retrieve an event organizer by user ID.
        """
        try:
            self.logger.info(f"Retrieving event organizer by user ID: {user_id}")
            result = await self.session.execute(
                select(EventOrganizer).filter(EventOrganizer.user_id == user_id)
            )
            organizer = result.scalars().first()
            return organizer
        except Exception as e:
            self.logger.error(f"Error retrieving organizer by user ID {user_id}: {str(e)}")
            raise
        
    async def get_organizers_by_status(self, status: List[OrganizerStatus]) -> List[EventOrganizer]:
        """
        Retrieve all event organizers by status.
        """
        try:
            self.logger.info(f"Retrieving organizers by status: {status}")
            result = await self.session.execute(
                select(EventOrganizer).filter(EventOrganizer.status.in_(status))
            )
            organizers = result.scalars().all()
            return organizers
        except Exception as e:
            self.logger.error(f"Error retrieving organizers by status {status}: {str(e)}")
            raise

    async def create_organizer(self, organizer: EventOrganizer) -> EventOrganizer:
        """
        Create a new event organizer.
        """
        try:
            self.logger.info("Creating new event organizer")
            self.session.add(organizer)
            self.logger.info(f"Created event organizer with ID: {organizer.organizer_id}")
            return organizer
        except Exception as e:
            self.logger.error(f"Error creating event organizer: {str(e)}")
            raise

    async def update_organizer(self, organizer_id: str, update_data: dict) ->  bool:
        """
        Update an existing event organizer.
        """
        try:
            self.logger.info(f"Updating event organizer with ID: {organizer_id}")
            stmt = update(EventOrganizer).where(EventOrganizer.organizer_id == organizer_id).values(**update_data)
            result = await self.session.execute(stmt)
            if result.rowcount == 0:
                self.logger.warning(f"Event organizer with ID {organizer_id} not found for update.")
                return False    
            
            self.logger.info(f"Updated event organizer with ID: {organizer_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error updating event organizer with ID {organizer_id}: {str(e)}")
            raise   
            

    async def delete_organizer(self, organizer_id: str) -> bool:
        """
        Delete an event organizer by ID.
        """
        try:
            organizer = await self.get_organizer_by_id(organizer_id)
            if not organizer:
                self.logger.warning(f"Organizer with ID {organizer_id} not found")
                return False

            await self.session.delete(organizer)
            await self.session.commit()
            self.logger.info(f"Deleted organizer with ID: {organizer_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting event organizer with ID {organizer_id}: {str(e)}")
            raise
