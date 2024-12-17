from fastapi import APIRouter, Depends, Response, Request, HTTPException, Form, File, UploadFile
from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user, get_optional_user
from app.core.config import Logger
from app.schemas.event_organizer import RequestOrganizer, ChangeOrganizerStatus, EventOrganizerResponse, EditOrganizer
from app.schemas.response import ResponseModel, ResponseSuccess
from datetime import datetime
from app.services.event_organizer_service import EventOrganizerService
from typing import Dict, Optional, Union
router = APIRouter()
logger = Logger(__name__).get_logger()


@router.get("/", response_model=EventOrganizerResponse)
async def get_all_organizers(
    db=Depends(get_db),
    current_user: Optional[Dict] = Depends(get_current_user)
):
    """
    Endpoint untuk mendapatkan semua Event Organizer.
    """
    service = EventOrganizerService(db)
    logger.debug("Received request to get all Event Organizers")
    try:
        response = await service.get_all_organizers(current_user)
        logger.info("All Event Organizers have been retrieved successfully")
        
        return response.model_dump()
    except HTTPException as e:
        logger.error(f"Error while getting all organizers: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error while getting all organizers: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/me")
async def get_my_organizer(
    db=Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    """
    Endpoint untuk mendapatkan Event Organizer milik user.
    """
    service = EventOrganizerService(db)
    logger.debug(f"Received request to get Event Organizer of user {current_user.get('sub')}")
    try:
        response = await service.get_my_organizer(current_user)
        logger.info(f"Event Organizer of user {current_user.get('sub')} has been retrieved successfully")
        return response.model_dump()
    except HTTPException as e:
        logger.error(f"Error while getting organizer: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error while getting organizer: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{organizer_id}")
async def get_organizer_by_id(
    organizer_id: str,
    db=Depends(get_db),
    current: Dict = Depends(get_optional_user)
):
    """
    Endpoint untuk mendapatkan Event Organizer berdasarkan ID.
    """
    service = EventOrganizerService(db)
    logger.debug(f"Received request to get Event Organizer {organizer_id}")
    try:
        response = await service.get_organizer_by_id(current, organizer_id)
        logger.info(f"Event Organizer {organizer_id} has been retrieved successfully")
        return response.model_dump()
    except HTTPException as e:
        logger.error(f"Error while getting organizer: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error while getting organizer: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/register", response_model=ResponseModel, status_code=201)
async def request_organizer(
    request: RequestOrganizer,
    db=Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    
    """
    Endpoint untuk user mengajukan request menjadi Event Organizer.
    """
    service = EventOrganizerService(db)
    logger.debug(f"Received request to become Event Organizer from user: {current_user.get('sub')}")
    try:
        response = await service.request_organizer(current_user.get('sub'), request)
        logger.info(f"Request to become Event Organizer from user {current_user.get('sub')} has been submitted successfully")
        return response.model_dump()
    except HTTPException as e:
        logger.error(f"Error while requesting organizer: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error while requesting organizer: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{organizer_id}/ change-status", response_model=ResponseModel)
async def change_organizer_status(
    organizer_id: str,
    request: ChangeOrganizerStatus,
    current_user: Dict = Depends(get_current_user),
    db=Depends(get_db)
):
    """
    Endpoint untuk mengubah status Event Organizer.
    """
    service = EventOrganizerService(db)
    logger.debug(f"Received request to change status of Event Organizer {organizer_id}")
    try:
        response = await service.change_organizer_status(organizer_id, request, current_user)
        logger.info(f"Status of Event Organizer {organizer_id} has been changed successfully")
        return response.model_dump()
    except HTTPException as e:
        logger.error(f"Error while changing status of organizer: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error while changing status of organizer: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/{organizer_id}/edit", response_model=ResponseSuccess)
async def edit_organizer(
    organizer_id: str,
    company_name: str = Form(None),
    company_address: str = Form(None),
    company_pic:str = Form(None),
    company_email: str = Form(None),
    company_phone: str = Form(None),
    company_experience: str = Form(None),
    company_portofolio: str = Form(None),
    profile_picture: Optional[UploadFile] = File(None),
    profile_picture_url: Optional[str] = Form(None),
    current_user: Dict = Depends(get_current_user),
    db=Depends(get_db)
):
    """
    Endpoint untuk mengubah data Event Organizer.
    """
    service = EventOrganizerService(db)
    logger.debug(f"Received request to edit Event Organizer {organizer_id}")
    try:
        request = EditOrganizer(
            company_name=company_name,
            company_address=company_address,
            company_pic=company_pic,
            company_email=company_email,
            company_phone=company_phone,
            company_experience=company_experience,
            company_portofolio=company_portofolio,
            profile_picture=profile_picture,
            profile_picture_url=profile_picture_url
        )
        response = await service.update_organizer(organizer_id, request, current_user)
        logger.info(f"Event Organizer {organizer_id} has been edited successfully")
        return response.model_dump()
    except ValueError as e:
        logger.error(f"Error while editing organizer: {e}")
        raise e
    except HTTPException as e:
        logger.error(f"Error while editing organizer: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error while editing organizer: {e}")
        raise HTTPException(status_code=500, detail=str(e))