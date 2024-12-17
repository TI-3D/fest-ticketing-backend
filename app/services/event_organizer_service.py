from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, UploadFile
from app.models import OrganizerStatus, EventOrganizer, Role
from app.repositories import EventOrganizerRepository, UserRepository, EventRepository
from app.schemas.event_organizer import RequestOrganizer, EditOrganizer, OrganizerBase, ChangeOrganizerStatus, EventOrganizerResponse, OrganizerDetailResponse
from app.schemas.event import EventBase
from app.core.config import Logger
from app.schemas.response import ResponseModel, ResponseSuccess
from typing import Dict
from app.services.cloudinary_service import CloudinaryService


class EventOrganizerService:
    def __init__(self, session: AsyncSession):
        self.organizer_repository = EventOrganizerRepository(session)
        self.user_repository = UserRepository(session)
        self.event_repository = EventRepository(session)
        self.session = session
        self.cloudinary_service = CloudinaryService()
        self.logger = Logger(__name__).get_logger()
        
    async def get_all_organizers(self, current: Dict) -> EventOrganizerResponse:
        async with self.session.begin():
            self.logger.info("Retrieving all Event Organizers")
            user = await self.user_repository.get_user_by_id(current.get("sub"))
            if user.role != Role.ADMIN:
                self.logger.warning(f"User {current.get('sub')} is not authorized to get all organizers")
                raise HTTPException(status_code=403, detail="Forbidden")
            organizers = await self.organizer_repository.get_all_organizers()
            organizers = [OrganizerBase.model_validate(organizer) for organizer in organizers]
            return EventOrganizerResponse(message="Event Organizers retrieved successfully", data=organizers)
        
    async def get_my_organizer(self, current: Dict) -> ResponseSuccess:
        async with self.session.begin():
            user = await self.user_repository.get_user_by_id(current.get("sub"))
            if user.role != Role.EO:
                self.logger.warning(f"User {current.get('sub')} is not authorized to get their organizer")
                raise HTTPException(status_code=403, detail="Forbidden")
            organizer = await self.organizer_repository.get_organizer_by_user_id(current.get("sub"))
            if not organizer:
                self.logger.warning(f"User {current.get('sub')} does not have an organizer")
                raise HTTPException(status_code=404, detail="Organizer not found")
            event = await self.event_repository.get_events_by_organizer_id(organizer.organizer_id)
            return ResponseSuccess(message="Event Organizer retrieved successfully", data={
                "organizer": OrganizerBase.model_validate(organizer),
                "events": [EventBase.model_validate(e) for e in event] if event else []
                })
        
    async def get_organizer_by_id(self, current:Dict, organizer_id: str) -> OrganizerDetailResponse:
        async with self.session.begin():
            self.logger.info(f"Retrieving Event Organizer {organizer_id}")
            organizer = await self.organizer_repository.get_organizer_by_id(organizer_id)
            user = await self.user_repository.get_user_by_id(current.get("sub"))
            if user and user.role == Role.ADMIN:
                return OrganizerDetailResponse(message="Event Organizer retrieved successfully", data=OrganizerBase.model_validate(organizer))
            if not organizer or organizer.status != OrganizerStatus.ACTIVE:
                self.logger.warning(f"Event Organizer {organizer_id} not found")
                raise HTTPException(status_code=404, detail="Organizer not found")
            return OrganizerDetailResponse(message="Event Organizer retrieved successfully", data=OrganizerBase.model_validate(organizer))
        
        
    async def request_organizer(self, user_id: str, data: RequestOrganizer) -> ResponseSuccess:
        async with self.session.begin():
            self.logger.info(f"User {user_id} is requesting to become an Event Organizer")
            
            # Pastikan user ada
            user = await self.user_repository.get_user_by_id(user_id)
            if not user:
                self.logger.warning(f"User {user_id} not found during organizer request")
                raise HTTPException(status_code=404, detail="User not found")

            # Cek apakah user sudah menjadi organizer
            existing_organizer = await self.organizer_repository.get_organizer_by_user_id(user_id)
            if existing_organizer:
                self.logger.warning(f"User {user_id} already has an organizer request")
                raise HTTPException(status_code=400, detail="User already has an organizer request")

            # Buat data Event Organizer
            organizer = EventOrganizer(
                user_id=user_id,
                company_name=data.company_name,
                company_address=data.company_address,
                company_pic=data.company_pic,
                company_phone=data.company_phone,
                company_email=data.company_email,
                company_experience=data.company_experience,
                company_portofolio=data.company_portofolio,
                status=OrganizerStatus.PENDING,  # Status default
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )

            organizer = await self.organizer_repository.create_organizer(organizer) 
            await self.user_repository.update_user_role(user_id, Role.EO)
            
            self.logger.info(f"Event Organizer request created successfully for user {user_id}")
            return ResponseSuccess(message="Event Organizer request submitted successfully", data={
                "organizer": OrganizerBase.model_validate(organizer),
                "events": []
            })

    async def update_organizer(self, organizer_id: str, data: EditOrganizer, current: Dict) -> ResponseSuccess:
        async with self.session.begin():
            
            self.logger.info(f"Updating Event Organizer {organizer_id}")
            user = await self.user_repository.get_user_by_id(current.get("sub"))
            if user.role not in [Role.ADMIN, Role.EO]:
                self.logger.warning(f"User {current.get('sub')} is not authorized to update organizer")
                raise HTTPException(status_code=403, detail="Forbidden")
            
            # Pastikan organizer ada
            organizer = await self.organizer_repository.get_organizer_by_id(organizer_id)
            if not organizer or organizer.status != OrganizerStatus.ACTIVE:
                self.logger.warning(f"Event Organizer {organizer_id} not found")
                raise HTTPException(status_code=404, detail="Organizer not found")

            # Update data organizer
            updated_data = data.model_dump(exclude_unset=True, exclude={"profile_picture", "profile_picture_url"})
            if data.profile_picture_url:
                updated_data["profile_picture"] = organizer.profile_picture
            elif data.profile_picture:
                image_url = self.cloudinary_service.upload_image(data.profile_picture.file.read(), folder_name="organizers")
                updated_data["profile_picture"] = image_url["secure_url"]
                if organizer.profile_picture is not None:
                    self.cloudinary_service.delete_image_by_url(organizer.profile_picture, folder_name="organizers")
            else:
                updated_data["profile_picture"] = None
                
            updated_data["updated_at"] = datetime.now(timezone.utc)
            await self.organizer_repository.update_organizer(organizer_id, updated_data)
            # Refresh the organizer object from the session to get the latest data
            await self.session.refresh(organizer)  # Ensures the object is updated with the latest data

            self.logger.info(f"Event Organizer {organizer_id} updated successfully")
            event = await self.event_repository.get_events_by_organizer_id(organizer.organizer_id)
            # Return the updated organizer as a response
            return ResponseSuccess(message="Event Organizer updated successfully", data={
                "organizer": OrganizerBase.model_validate(organizer),
                "events": [EventBase.model_validate(e) for e in event] if event else []
            })
        
    async def change_organizer_status(self, organizer_id: UUID, data: ChangeOrganizerStatus, current_user: dict) -> ResponseModel:
        async with self.session.begin():
            user = await self.user_repository.get_user_by_id(current_user.get("sub"))
            if user.role != Role.ADMIN:
                self.logger.warning(f"User {current_user.get('sub')} is not authorized to change organizer status")
                raise HTTPException(status_code=403, detail="Forbidden")
            self.logger.info(f"Changing status of Event Organizer {organizer_id}")

            organizer = await self.organizer_repository.get_organizer_by_id(organizer_id)
            if not organizer:
                self.logger.warning(f"Event Organizer {organizer_id} not found")
                raise HTTPException(status_code=404, detail="Organizer not found")
            if organizer.status in [OrganizerStatus.ACTIVE, OrganizerStatus.PENDING]:
                await self.user_repository.update_user_role(organizer.user_id, Role.EO)
            else:
                await self.user_repository.update_user_role(organizer.user_id, Role.USER)
            # Update status organizer
            updated_data = {"status": data.status, "updated_at": datetime.now(timezone.utc)}
            await self.organizer_repository.update_organizer(organizer_id, updated_data)

            self.logger.info(f"Status of Event Organizer {organizer_id} changed successfully")
            return ResponseModel(message="Status of Event Organizer changed successfully")
