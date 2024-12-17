from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models import Role, Event, EventCategories, EventStatus, OrganizerStatus, EventClass, EventCategoryAssociation
from app.repositories import EventOrganizerRepository, UserRepository, EventRepository
from app.schemas.event import EventResponse, EventBase, EventCreate, EventUpdate, ChangeEventStatus
from app.core.config import Logger
from app.schemas.response import ResponseModel, ResponseSuccess
from typing import Dict
from app.services.cloudinary_service import CloudinaryService

class EventService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repository = UserRepository(session)
        self.event_repository = EventRepository(session)
        self.organizer_repository = EventOrganizerRepository(session)
        self.cloudinary_service = CloudinaryService()
        self.logger = Logger(__name__).get_logger()
        
    async def get_all_event_categories(self) -> ResponseSuccess:
        async with self.session.begin():
            self.logger.info("Retrieving all Event Categories")
            categories = await self.event_repository.get_all_categories()
            return ResponseSuccess(message="Event Categories retrieved successfully", data=categories)
        
    async def get_all_events(self, current: Dict = None) -> EventResponse:
        async with self.session.begin():
            self.logger.info("Retrieving all Events")

            # If no user is provided, fetch all events
            if not current:
                events = await self.event_repository.get_events_by_status([EventStatus.ACTIVE, EventStatus.COMPLETED, EventStatus.CANCELLED])
                print(events)
            else:
                user = await self.user_repository.get_user_by_id(current.get("sub"))
                # Fetch events by status based on the current's role
                if user.role == Role.EO:  # Event Organizer
                    self.logger.info(f"Retrieving events for Event Organizer {current.get('sub')}")
                    organizer = await self.organizer_repository.get_organizer_by_user_id(current.get("sub"))
                    events = await self.event_repository.get_events_by_organizer(organizer.organizer_id, [EventStatus.ACTIVE, EventStatus.COMPLETED, EventStatus.CANCELLED])
                elif user.role == Role.ADMIN:  # Admin
                    self.logger.info(f"Retrieving events for Admin {current.get('sub')}")
                    events = await self.event_repository.get_events_by_status([EventStatus.ACTIVE, EventStatus.COMPLETED, EventStatus.CANCELLED])
                else:
                    self.logger.warning(f"User {current.get('sub')} has an unauthorized role")
                    events = []
                    
            if not events:
                self.logger.warning(f"No events found for user {current.get('sub') if current else 'unknown'}")
                raise HTTPException(status_code=404, detail="No events found")

            return EventResponse(message="Events retrieved successfully", data=[EventBase.model_validate(event) for event in events])
    
    async def create_event(self, event: EventCreate, currentuser: Dict) -> ResponseSuccess:
        """
        Create an event.
        """
        try:
            # Check if the user is an Event Organizer
            organizer = await self.organizer_repository.get_organizer_by_user_id(currentuser.get("sub"))
            if not organizer or organizer.status != OrganizerStatus.ACTIVE:
                self.logger.error(f"Organizer not found or not active for user: {currentuser.get('sub')}")
                raise HTTPException(status_code=403, detail="Forbidden")

            # Log incoming event data
            self.logger.info(f"Creating event with name: {event.name}")

            # Begin a transaction block (do not nest transactions within an already started transaction)
            image_url = self.cloudinary_service.upload_image(event.image.file.read(), folder_name="events")
            event_data = Event(
                name=event.name,
                description=event.description,
                organizer=organizer,
                date=event.date,
                image=image_url["secure_url"],
                location=event.location,
            )
                # Add event to repository and commit
            created_event = await self.event_repository.create_event(event_data)
            await self.session.commit()
            
            for event_class in event.event_classes:
                event_class_data = EventClass(
                    event_id=created_event.event_id,
                    class_name=event_class.class_name,
                    base_price=event_class.base_price,
                    count=event_class.count
                )
                await self.event_repository.create_event_class(event_class_data)
                await self.session.commit()
            
            # Add event categories
            for category in event.categories:
                # Check if category exists
                category_exists = await self.event_repository.get_categories_by_name(category)
                if category_exists:
                    # If category exists, create association
                    association = EventCategoryAssociation(event_id=created_event.event_id, category_name=category)
                    await self.event_repository.create_event_category_association(association)
                    await self.session.commit()
                    
            
            event = await self.event_repository.get_event_by_id(created_event.event_id)
            
            # Return success response
            return ResponseSuccess(message="Event created successfully", data=EventBase.model_validate(event))  
            
        except Exception as e:
            # Log error with full details
            self.logger.error(f"Error creating event: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error creating event: {str(e)}")

    async def update_event(self, event: EventUpdate, currentuser: Dict) -> ResponseSuccess:
        """
        Update an event.
        """
        try:
            # Check if the user is an Event Organizer
            organizer = await self.organizer_repository.get_organizer_by_user_id(currentuser.get("sub"))
            if not organizer or organizer.status != OrganizerStatus.ACTIVE:
                self.logger.error(f"Organizer not found or not active for user: {currentuser.get('sub')}")
                raise HTTPException(status_code=403, detail="Forbidden")

            # Log incoming event data
            self.logger.info(f"Updating event with ID: {event.event_id}")
            
            event_data = await self.event_repository.get_event_by_id(event.event_id)
            if not event_data:
                self.logger.error(f"Event not found with ID: {event.event_id}")
                raise HTTPException(status_code=404, detail="Event not found")
            
            if event.image:
                image_url = self.cloudinary_service.upload_image(event.image.file.read(), folder_name="events")
                if event_data.image:
                    self.cloudinary_service.delete_image_by_url(event_data.image, folder_name="events")
                
                event.image = image_url['secure_url']
            # Update event data
            event_data.name = event.name
            event_data.description = event.description
            event_data.date = event.date
            
            # Update event classes
            for event_class in event.event_classes:
                event_class_data = await self.event_repository.get_event_class_by_id_and_name(event.event_id, event_class.class_name)
                if event_class_data:
                    # Update existing event class
                    event_class_data.class_name = event_class.class_name
                    event_class_data.base_price = event_class.base_price
                    event_class_data.count = event_class.count
                    event_class_data.description = event_class.description
                else:
                    # Create new event class
                    new_event_class = EventClass(
                        event_id=event.event_id,
                        class_name=event_class.class_name,
                        base_price=event_class.base_price,
                        count=event_class.count,
                        description=event_class.description
                    )
                    await self.event_repository.create_event_class(new_event_class)
                await self.session.commit()
                    
                
            # Update event categories
            for category in event.categories:
                # Check if category exists and delete if not in the list
                category_exists = await self.event_repository.get_categories_by_name(category)
                if category_exists:
                    # If category exists, create association
                    association = EventCategoryAssociation(event_id=event.event_id, category_name=category)
                    await self.event_repository.create_event_category_association(association)
                    await self.session.commit()
                else:
                    # Delete association
                    await self.event_repository.delete_event_category_association(event.event_id, category)
                    await self.session.commit()
                    
            # Commit changes
            await self.session.commit()
            
            # Return success response
            return ResponseSuccess(message="Event updated successfully", data=EventBase.model_validate(event_data))
        except Exception as e:
            
            await self.session.rollback()
            # Log error with full details
            self.logger.error(f"Error creating event: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error creating event: {str(e)}")


    
    async def get_event_by_id(self, event_id: str, current: Dict = None) -> ResponseSuccess:
        """
        Retrieves an event by its ID, checking the user's role and status.
        """
        try:
            # Check user role and fetch event details accordingly.
            user = await self.user_repository.get_user_by_id(current.get("sub")) if current else None
            if user and user.role == Role.EO:  # Event Organizer
                self.logger.info(f"Retrieving Event {event_id} for Event Organizer {current.get('sub')}")
                # Get organizer info
                organizer = await self.organizer_repository.get_organizer_by_user_id(current.get("sub"))
                # Fetch event based on organizer's ID
                event = await self.event_repository.get_event_by_id(event_id, organizer.organizer_id)
            elif user and user.role == Role.ADMIN:  # Admin
                self.logger.info(f"Retrieving Event {event_id} for Admin {current.get('sub')}")
                # Fetch event for admin
                event = await self.event_repository.get_event_by_id(event_id)
            else:
                event = await self.event_repository.get_event_detail_by_status(event_id, [EventStatus.ACTIVE, EventStatus.CANCELLED, EventStatus.COMPLETED])

            # If no event is found, raise an HTTPException
            if not event:
                self.logger.warning(f"Event {event_id} not found")
                raise HTTPException(status_code=404, detail="Event not found")

            # Return event response with event data validation
            return ResponseSuccess(message="Event retrieved successfully", data=EventBase.model_validate(event))

        except Exception as e:
            # Log unexpected errors
            self.logger.error(f"Error retrieving event {event_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
    
    
    async def change_event_status(self, event_id:str, event_status: ChangeEventStatus, current: Dict) -> ResponseSuccess:
        """
        Change the status of an event.
        """
        try:
            # Check if the user is an Event Organizer
            user = await self.user_repository.get_user_by_id(current.get("sub"))
            if not user or user.role not in [Role.EO, Role.ADMIN]:
                self.logger.error(f"User {current.get('sub')} is not an Event Organizer")
                raise HTTPException(status_code=403, detail="Forbidden")
            
            if user.role == Role.EO:
                # Get organizer info
                organizer = await self.organizer_repository.get_organizer_by_user_id(current.get("sub"))
                # Fetch event based on organizer's ID
                event = await self.event_repository.get_event_by_id(event_id)
                if not event or event.organizer_id != organizer.organizer_id:
                    self.logger.error(f"Event {event_status.event_id} not found or unauthorized")
                    raise HTTPException(status_code=404, detail="Event not found")
                
                # Update event status
                if event_status.status in [EventStatus.CANCELLED, EventStatus.COMPLETED]:
                    await self.event_repository.update_status(event_status.event_id, event_status.status)
            
            elif user.role == Role.ADMIN:
                event = await self.event_repository.get_event_by_id(event_status.event_id)
                if not event:
                    self.logger.error(f"Event {event_status.event_id} not found")
                    raise HTTPException(status_code=404, detail="Event not found")
                
                await self.event_repository.update_status(event_status.event_id, event_status.status)
            
            return ResponseSuccess(message="Event status updated successfully", data=EventBase.model_validate(event))
        except Exception as e:
            await self.session.rollback()
            self.logger.error(f"Error updating event status: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")