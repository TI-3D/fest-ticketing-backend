from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user, get_optional_user
from app.core.config import Logger
from app.schemas.response import ResponseSuccess
from typing import Dict, Optional, List
from app.services.event_service import EventService
from app.schemas.event import EventCreate, EventClassCreate, EventUpdate, ChangeEventStatus
from datetime import datetime


router = APIRouter()
logger = Logger(__name__).get_logger()


@router.get("/categories", response_model=ResponseSuccess)
async def get_all_organizers(
    db = Depends(get_db)
):
    event_service = EventService(db)    
    try:
        response = await event_service.get_all_event_categories()
        logger.info("Event Categories retrieved successfully")
        return response.model_dump()
    except HTTPException as e:
        logger.error(f"Error getting all organizers: {str(e.detail)}")
        return e
    except Exception as e:
        logger.error(f"Error getting all organizers: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.post("", status_code=201)
async def create_event(
    name: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    categories: List[str] = Form(...),
    event_classes_class_name: List[str] = Form(...),
    event_classes_base_price: List[int] = Form(...),
    event_classes_count: List[int] = Form(...),
    
    date: datetime = Form(...),
    image: UploadFile = File(...),
    current_user: Dict = Depends(get_current_user),
    db = Depends(get_db)
    ):
    
    event_service = EventService(db)
    try:  
        event_classes = [
            EventClassCreate(
                class_name=event_classes_class_name[i],
                base_price=event_classes_base_price[i],
                count=event_classes_count[i]
            )
            for i in range(len(event_classes_class_name))
        ]
        
        print(image.filename)
        print(image.content_type)
        print(image.size)
        event_create = EventCreate(
            name=name,
            description=description,
            location=location,
            categories=categories,
            event_classes=event_classes,
            date=date,
            image=image
        )
        
        
        
        
        response = await event_service.create_event(event_create, current_user)
        logger.info("Event created successfully")
        return response.model_dump()
    except HTTPException as e:
        logger.error(f"Error creating event: {str(e.detail)}")
        raise e
    except Exception as e:
        logger.error(f"Error creating event: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.put("/{event_id}", status_code=200)
async def update_event(
    event_id: str,
    name: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    categories: List[str] = Form(...),
    event_classes_class_name: List[str] = Form(...),
    event_classes_base_price: List[int] = Form(...),
    event_classes_count: List[int] = Form(...),
    date: datetime = Form(...),
    image: UploadFile = File(...),
    current_user: Dict = Depends(get_current_user),
    db = Depends(get_db)
    ):
    
    event_service = EventService(db)
    try:  
        event_classes = [
            EventClassCreate(
                class_name=event_classes_class_name[i],
                base_price=event_classes_base_price[i],
                count=event_classes_count[i]
            )
            for i in range(len(event_classes_class_name))
        ]
        event_create = EventUpdate(
            event_id=event_id,
            name=name,
            description=description,
            location=location,
            categories=categories,
            event_classes=event_classes,
            date=date,
            image=image
        )
        
        
        response = await event_service.update_event(event_create, current_user)
        logger.info("Event updated successfully")
        return response.model_dump()
    except HTTPException as e:
        logger.error(f"Error updating event: {str(e.detail)}")
        raise e
    except Exception as e:
        logger.error(f"Error updating event: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("", response_model=ResponseSuccess)
async def get_all_event(
    db = Depends(get_db)
):
    event_service = EventService(db)
    try:
        response = await event_service.get_all_events()
        logger.info("Events retrieved successfully")
        return response.model_dump()
    except HTTPException as e:
        logger.error(f"Error getting all events: {str(e.detail)}")
        raise e
    except Exception as e:
        logger.error(f"Error getting all events: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
    
@router.get("/{event_id}", response_model=ResponseSuccess)
async def get_event_by_id(
    event_id: str,
    optional_user: Optional[Dict] = Depends(get_optional_user),
    db = Depends(get_db)
):
    event_service = EventService(db)
    try:
        response = await event_service.get_event_by_id(event_id, optional_user)
        logger.info(f"Event {event_id} retrieved successfully")
        return response.model_dump()
    except HTTPException as e:
        logger.error(f"Error getting event {event_id}: {str(e.detail)}")
        raise e
    except Exception as e:
        logger.error(f"Error getting event {event_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@router.patch("/{event_id}/change_status", status_code=200)
async def change_event_status(
    event_id: str,
    status: ChangeEventStatus,
    current_user: Dict = Depends(get_current_user),
    db = Depends(get_db)
):
    event_service = EventService(db)
    try:
        response = await event_service.change_event_status(event_id, status, current_user)
        logger.info(f"Event {event_id} status changed successfully")
        return response.model_dump()
    except HTTPException as e:
        logger.error(f"Error changing event {event_id} status: {str(e.detail)}")
        raise e
    except Exception as e:
        logger.error(f"Error changing event {event_id} status: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    