from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload
from typing import List, Optional
from uuid import UUID
from app.models import Event, EventStatus, EventCategories, EventClass, EventCategoryAssociation
from app.core.config import Logger

class EventRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = Logger(__name__).get_logger()
        
    async def get_categories_by_name(self, category_names: str) -> EventCategories:
        """
        Retrieve event categories by name.
        """
        try:
            self.logger.info(f"Attempting to retrieve categories by names: {category_names}")
            result = await self.session.execute(
                select(EventCategories)
                .filter(EventCategories.category_name == category_names)
            )
            categories = result.scalars().all()
            return categories
        except Exception as e:
            self.logger.error(f"Error retrieving categories by names {category_names}: {str(e)}")
            raise
    
    async def get_all_categories(self) -> List[str]:
        """
        Retrieve all event categories.
        """
        try:
            self.logger.info("Attempting to retrieve all event categories")
            result = await self.session.execute(select(EventCategories.category_name))
            categories = result.scalars().all()
            return categories
        except Exception as e:
            self.logger.error(f"Error retrieving all event categories: {str(e)}")
            raise

    async def get_all_events(self) -> List[Event]:
        """
        Retrieve all events.
        """
        try:
            self.logger.info("Attempting to retrieve all events")
            result = await self.session.execute(
                select(Event)
                .options(joinedload(Event.categories))
                .options(joinedload(Event.organizer))
                .options(joinedload(Event.event_classes))
                .order_by(Event.updated_at.desc())
            )
            events = result.unique().scalars().all()
            return events
        except Exception as e:
            self.logger.error(f"Error retrieving all events: {str(e)}")
            raise

    async def get_event_by_id(self, event_id: UUID) -> Optional[Event]:
        """
        Retrieve an event by its ID.
        """
        try:
            self.logger.info(f"Retrieving event with ID: {event_id}")
            result = await self.session.execute(
                select(Event)
                .options(joinedload(Event.categories))
                .options(joinedload(Event.organizer))
                .options(joinedload(Event.event_classes))
                .filter(Event.event_id == event_id)
            )
            event = result.unique().scalars().first()
            return event
        except Exception as e:
            self.logger.error(f"Error retrieving event by ID {event_id}: {str(e)}")
            raise
    async def get_event_detail_on_organizer(self, event_id: UUID, organizer_id: UUID) -> Optional[Event]:
        """
        Retrieve an event by its ID and organizer ID.
        """
        try:
            self.logger.info(f"Retrieving event with ID: {event_id} and organizer ID: {organizer_id}")
            result = await self.session.execute(
                select(Event)
                .options(joinedload(Event.categories))
                .options(joinedload(Event.organizer))
                .options(joinedload(Event.event_classes))
                .filter(Event.event_id == event_id)
                .filter(Event.organizer_id == organizer_id)
            )
            event = result.unique().scalars().first()
            return event
        except Exception as e:
            self.logger.error(f"Error retrieving event by ID {event_id} and organizer ID {organizer_id}: {str(e)}")
            raise
    async def get_event_detail_by_status(self, event_id: UUID, status: List[EventStatus]) -> Optional[Event]:
        """
        Retrieve an event by its ID and status.
        """
        try:
            self.logger.info(f"Retrieving event with ID: {event_id} and status: {status}")
            result = await self.session.execute(
                select(Event)
                .options(joinedload(Event.categories))
                .options(joinedload(Event.organizer))
                .options(joinedload(Event.event_classes))
                .filter(Event.event_id == event_id)
                .filter(Event.status.in_(status))
            )
            event = result.unique().scalars().first()
            return event
        except Exception as e:
            self.logger.error(f"Error retrieving event by ID {event_id} and status {status}: {str(e)}")
            raise
        
    async def get_events_by_status(self, status: List[EventStatus]) -> List[Event]:
        """
        Retrieve all events by status.
        """
        try:
            self.logger.info(f"Retrieving events by status: {status}")
            result = await self.session.execute(
                select(Event)
                .filter(Event.status.in_(status))
                .options(joinedload(Event.categories))
                .options(joinedload(Event.organizer))
                .options(joinedload(Event.event_classes))
                .order_by(Event.updated_at.desc())
            )
            events = result.unique().scalars().all()
            if not events:
                from fastapi import HTTPException
                self.logger.warning(f"No events found with status: {status}")
                raise HTTPException(status_code=404, detail="No events found for the given status")
            self.logger.info(f"Retrieved {len(events)} events for status: {status}")
            return events
        except Exception as e:
            self.logger.error(f"Error retrieving events by status {status}: {str(e)}")
            raise

    async def get_events_by_organizer_id(self, organizer_id: UUID) -> List[Event]:
        """
        Retrieve all events by organizer ID.
        """
        try:
            self.logger.info(f"Retrieving events by organizer ID: {organizer_id}")
            result = await self.session.execute(
                select(Event).filter(Event.organizer_id == organizer_id)
                .options(joinedload(Event.categories))
                .options(joinedload(Event.organizer))
                .options(joinedload(Event.event_classes))
                .order_by(Event.updated_at.desc())
            )
            events = result.unique().scalars().all()
            return events
        except Exception as e:
            self.logger.error(f"Error retrieving events by organizer ID {organizer_id}: {str(e)}")
            raise

    async def create_event(self, event: Event) -> Event:
        """
        Create a new event.
        """
        try:
            self.logger.info("Creating new event")
            self.session.add(event)  # Just add the event to the session
            return event  # Return the event without committing
        except Exception as e:
            self.logger.error(f"Error creating event: {str(e)}")
            raise

    async def update_event(self, event_id: UUID, update_data: dict) -> bool:
        """
        Update an existing event.
        """
        try:
            self.logger.info(f"Updating event with ID: {event_id}")
            stmt = update(Event).where(Event.event_id == event_id).values(**update_data)
            result = await self.session.execute(stmt)
            if result.rowcount == 0:
                self.logger.warning(f"Event with ID {event_id} not found for update.")
                return False

            self.logger.info(f"Updated event with ID: {event_id}")
            await self.session.commit()  # Commit the changes
            return True
        except Exception as e:
            self.logger.error(f"Error updating event with ID {event_id}: {str(e)}")
            raise

    async def delete_event(self, event_id: UUID) -> bool:
        """
        Delete an event by ID.
        """
        try:
            event = await self.get_event_by_id(event_id)
            if not event:
                self.logger.warning(f"Event with ID {event_id} not found")
                return False

            await self.session.delete(event)
            await self.session.commit()  # Commit the deletion
            self.logger.info(f"Deleted event with ID: {event_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting event with ID {event_id}: {str(e)}")
            raise
        
        
    async def create_event_class(self, event_class_data: EventClass) -> EventClass:
        """
        Create a new event class.
        """
        try:
            self.logger.info("Creating new event class")
            self.session.add(event_class_data)  # Just add the event class to the session
            return event_class_data  # Return the event class without committing
        except Exception as e:
            self.logger.error(f"Error creating event class: {str(e)}")
            raise
        
    async def create_event_category_association(self, association: EventCategoryAssociation) -> EventCategoryAssociation:
        """
        Create a new event category association.
        """
        try:
            self.logger.info("Creating new event category association")
            self.session.add(association)  # Just add the association to the session
            return association  # Return the association without committing
        except Exception as e:
            self.logger.error(f"Error creating event category association: {str(e)}")
            raise
    
    async def get_event_class_by_id_and_name(self, event_id: UUID, class_name: str) -> EventClass:
        """
        Retrieve an event class by event ID and class name.
        """
        try:
            self.logger.info(f"Retrieving event class by event ID {event_id} and class name {class_name}")
            result = await self.session.execute(
                select(EventClass)
                .filter(EventClass.event_id == event_id)
                .filter(EventClass.class_name == class_name)
            )
            event_class = result.scalars().first()
            return event_class
        except Exception as e:
            self.logger.error(f"Error retrieving event class by event ID {event_id} and class name {class_name}: {str(e)}")
    
    
    
    async def delete_event_category_association(self, event_id: UUID, category_name: str) -> bool:
        """
        Delete an event category association by event ID and category name.
        """
        try:
            self.logger.info(f"Deleting event category association for event ID {event_id} and category {category_name}")
            result = await self.session.execute(
                select(EventCategoryAssociation)
                .filter(EventCategoryAssociation.event_id == event_id)
                .filter(EventCategoryAssociation.category_name == category_name)
            )
            association = result.scalars().first()
            if not association:
                self.logger.warning(f"Event category association for event ID {event_id} and category {category_name} not found")
                return False

            await self.session.delete(association)
            await self.session.commit()  # Commit the deletion
            self.logger.info(f"Deleted event category association for event ID {event_id} and category {category_name}")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting event category association for event ID {event_id} and category {category_name}: {str(e)}")
            raise
        
    async def update_status(self, event_id: UUID, status: EventStatus) -> bool:
        """
        Update the status of an event.
        """
        try:
            self.logger.info(f"Updating status for event with ID {event_id}")
            stmt = update(Event).where(Event.event_id == event_id).values(status=status)
            result = await self.session.execute(stmt)
            if result.rowcount == 0:
                self.logger.warning(f"Event with ID {event_id} not found for status update.")
                return False

            self.logger.info(f"Updated status for event with ID {event_id}")
            await self.session.commit()  # Commit the changes
            return True
        except Exception as e:
            self.logger.error(f"Error updating status for event with ID {event_id}: {str(e)}")
            raise
        
    async def update_event_status(self, event_id: UUID, status: EventStatus) -> bool:
        """
        Update the status of an event.
        """
        try:
            self.logger.info(f"Updating status for event with ID {event_id}")
            stmt = update(Event).where(Event.event_id == event_id).values(status=status)
            result = await self.session.execute(stmt)
            if result.rowcount == 0:
                self.logger.warning(f"Event with ID {event_id} not found for status update.")
                return False

            self.logger.info(f"Updated status for event with ID {event_id}")
            await self.session.commit()  # Commit the changes
            return True
        except Exception as e:
            self.logger.error(f"Error updating status for event with ID {event_id}: {str(e)}")
            raise