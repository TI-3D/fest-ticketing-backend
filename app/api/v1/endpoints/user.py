from fastapi import APIRouter, Depends, Response, Request, HTTPException
from app.services.auth_service import AuthService
from app.dependencies.auth import  get_current_user
from app.dependencies.database import get_db
from app.core.config import Logger
from app.schemas.response import ResponseModel, ResponseSuccess
from typing import Dict, Optional
from fastapi import Form, File, UploadFile
from app.services.user_service import UserService
from app.schemas.user import EditUserProfile
from app.models import Gender
from datetime import datetime

router = APIRouter()
logger = Logger(__name__).get_logger()

@router.patch("/edit", response_model=ResponseSuccess)
async def edit_user(
    full_name: Optional[str] = Form(None),
    phone_number: Optional[str] = Form(None),
    birth_date: Optional[datetime] = Form(None),
    gender: Optional[Gender] = Form(None),
    address: Optional[str] = Form(None),
    profile_picture: Optional[UploadFile] = File(None),
    db=Depends(get_db),
    current_user: Dict = Depends(get_current_user)
):
    """
    Endpoint untuk mengedit data user.
    """
    service = UserService(db)
    logger.debug(f"Received request to edit user {current_user.get('sub')}")
    try:
        edit_user = EditUserProfile(
            full_name=full_name,
            birth_date=birth_date,
            phone_number=phone_number,
            gender=gender,
            address=address,
            profile_picture=profile_picture)
        print("edit_user", edit_user)
        response = await service.update_user(edit_user, current_user)
        logger.info(f"User {current_user.get('sub')} has been edited successfully")
        return response.model_dump()
    except HTTPException as e:
        logger.error(f"Error while editing user: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error while editing user: {e}")
        raise HTTPException(status_code=500, detail=str(e))