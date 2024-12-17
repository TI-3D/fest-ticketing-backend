from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from app.models import OrganizerStatus
from pydantic import BaseModel,  field_validator
from app.schemas.response import ResponseSuccess
from fastapi import UploadFile


class RequestOrganizer(BaseModel):
    company_name: str
    company_address: str
    company_pic: str
    company_email: EmailStr
    company_phone: str
    company_experience: str
    company_portofolio: str
    
    @field_validator('company_name')
    def validate_company_name(cls, v):
        if len(v) < 3:
            raise ValueError("Company name must be at least 3 characters long")
        return v
    
    @field_validator('company_address')
    def validate_company_address(cls, v):
        if len(v) < 10:
            raise ValueError("Company address must be at least 10 characters long")
        return v

    @field_validator('company_pic')
    def validate_company_pic(cls, v):
        if len(v) < 3:
            raise ValueError("Company PIC must be at least 3 characters long")
        return v
    
    @field_validator('company_email')
    def validate_company_email(cls, v):
        if not v.strip():
            raise ValueError("Email cannot be empty")
        if len(v) > 255:
            raise ValueError("Email must be less than 255 characters")
        return v
    
    @field_validator('company_phone')
    def validate_company_phone(cls, v):
        if len(v) < 10:
            raise ValueError("Company phone number must be at least 10 characters long")
        return v
    
    @field_validator('company_experience')
    def validate_company_experience(cls, v):
        if len(v) < 10:
            raise ValueError("Company experience must be at least 10 characters long")
        return v
    
    @field_validator('company_portofolio')
    def validate_company_portofolio(cls, v):
        # Must be a valid URL
        if not v.startswith("http"):
            raise ValueError("Company portofolio must be a valid URL")
        return v


class EditOrganizer(BaseModel):
    company_name: Optional[str] = None
    company_address: Optional[str] = None
    company_pic: str
    company_email: EmailStr
    company_phone: str
    company_experience: str
    company_portofolio: str
    profile_picture: Optional[UploadFile] = None
    profile_picture_url: Optional[str] = None
    
    @field_validator('company_name')
    def validate_company_name(cls, v):
        if not v:
            raise ValueError("Company name cannot be empty")
        if v and len(v) < 3:
            raise ValueError("Company name must be at least 3 characters long")
        return v
    
    @field_validator('company_address')
    def validate_company_address(cls, v):
        if not v:
            raise ValueError("Company address cannot be empty")
        if v and len(v) < 10:
            raise ValueError("Company address must be at least 10 characters long")
        return v

    @field_validator('company_pic')
    def validate_company_pic(cls, v):
        if len(v) < 3:
            raise ValueError("Company PIC must be at least 3 characters long")
        return v
    
    @field_validator('company_email')
    def validate_company_email(cls, v):
        if not v.strip():
            raise ValueError("Email cannot be empty")
        if len(v) > 255:
            raise ValueError("Email must be less than 255 characters")
        return v
    
    @field_validator('company_phone')
    def validate_company_phone(cls, v):
        if len(v) < 10:
            raise ValueError("Company phone number must be at least 10 characters long")
        return v
    
    @field_validator('company_experience')
    def validate_company_experience(cls, v):
        if len(v) < 10:
            raise ValueError("Company experience must be at least 10 characters long")
        return v
    
    @field_validator('company_portofolio')
    def validate_company_portofolio(cls, v):
        # Must be a valid URL
        if not v.startswith("http"):
            raise ValueError("Company portofolio must be a valid URL")
        return v
    
    @field_validator('profile_picture')
    def validate_profile_picture(cls, v):
        if not v:
            return None
        if isinstance(v, UploadFile):
            if not v.content_type.startswith("image"):
                raise ValueError("Profile picture must be an image")
            if not v.size < 5 * 1024 * 1024:
                raise ValueError("Profile picture must be less than 5MB")
            if not v.filename.endswith(('.jpg', '.jpeg', '.png')):
                raise ValueError("Profile picture must be a valid image format")
            return v
        
    @field_validator('profile_picture_url')
    def validate_profile_picture(cls, v):
        if not v:
            return None
        if isinstance(v, str):
            return v
    
    
class ChangeOrganizerStatus(BaseModel):
    status: OrganizerStatus
    
    @field_validator('status')
    def validate_status(cls, v):
        if not isinstance(v, OrganizerStatus):
            raise ValueError("Status must be an instance of OrganizerStatus")
        return v


class OrganizerBase(BaseModel):
    organizer_id: UUID
    company_name: str
    company_address: str
    company_pic: str
    company_email: EmailStr
    company_phone: str
    company_experience: str
    company_portofolio: str
    status: OrganizerStatus
    profile_picture: Optional[str]
    user_id: UUID
    created_at: datetime
    updated_at: datetime      
    
    @field_validator('organizer_id', 'user_id', mode="before")
    def validate_organizer_id(cls, v):
        if not isinstance(v, UUID):
            raise ValueError("Identifier ID must be a valid UUID")
        return v
    
    @field_validator('company_name')
    def validate_company_name(cls, v):
        if len(v) < 3:
            raise ValueError("Company name must be at least 3 characters long")
        return v
    
    @field_validator('company_address')
    def validate_company_address(cls, v):
        if len(v) < 10:
            raise ValueError("Company address must be at least 10 characters long")
        return v
    
    @field_validator('company_pic', mode="before")
    def validate_company_pic(cls, v):
        if len(v) < 3:
            raise ValueError("Company PIC must be at least 3 characters long")
        return v
    
    @field_validator('company_email', mode="before")
    def validate_company_email(cls, v):
        if not v.strip():
            raise ValueError("Email cannot be empty")
        if len(v) > 255:
            raise ValueError("Email must be less than 255 characters")
        return v
    
    @field_validator('company_phone', mode="before")
    def validate_company_phone(cls, v):
        if len(v) < 10:
            raise ValueError("Company phone number must be at least 10 characters long")
        return v
    
    @field_validator('company_experience', mode="before")
    def validate_company_experience(cls, v):
        if len(v) < 10:
            raise ValueError("Company experience must be at least 10 characters long")
        return v
    
    @field_validator('company_portofolio', mode="before")
    def validate_company_portofolio(cls, v):
        # Must be a valid URL
        if not v.startswith("http"):
            raise ValueError("Company portofolio must be a valid URL")
        return v
    
    @field_validator('status', mode="before")
    def validate_status(cls, v):
        if not isinstance(v, OrganizerStatus):
            raise ValueError("Status must be an instance of OrganizerStatus")
        return v
    
    
    @field_validator("created_at", "updated_at", mode="before")
    def validate_datetime_fields(cls, v):
        if not isinstance(v, datetime):
            raise ValueError("Field must be a valid datetime object")
        return v.isoformat()

    class Config:
        from_attributes = True


class EventOrganizerResponse(ResponseSuccess):
    data: List[OrganizerBase] | OrganizerBase
    
    @field_validator('data')
    def validate_data(cls, v):
        if isinstance(v, List) or isinstance(v, OrganizerBase):
            return v
        raise ValueError("Data must be a list of OrganizerBase or a single OrganizerBase")

class OrganizerDetailResponse(ResponseSuccess):
    data: OrganizerBase
    
    @field_validator('data')
    def validate_data(cls, v):
        if isinstance(v, OrganizerBase):
            return v
        raise ValueError("Data must be a single OrganizerBase")