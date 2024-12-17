from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
from app.models import Gender, Role
from datetime import datetime
from typing import Optional
from fastapi import UploadFile
class UserBase(BaseModel):
    user_id: UUID
    full_name: str
    email: EmailStr
    gender: Optional[Gender] = None
    birth_date: Optional[datetime]
    phone_number: Optional[str]
    nik: Optional[str]
    address: Optional[str]
    role: Role
    embedding: Optional[str] = None
    profile_picture: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    @field_validator("gender", mode="before")
    def validate_gender(cls, v):
        if not isinstance(v, Gender):
            raise ValueError("Gender must be a valid Gender enum")
        return v
    
    @field_validator("role", mode="before")
    def validate_role(cls, v):
        if not isinstance(v, Role):
            raise ValueError("Role must be a valid Role enum")
        return v
    
    @field_validator("user_id", mode="before")
    def validate_user_id(cls, v):
        if not isinstance(v, UUID):
            ValueError("User ID must be a valid UUID")
        return str(v)

    @field_validator("birth_date", "created_at", "updated_at", mode="before")
    def validate_datetime_fields(cls, v):
        if not v:
            return None
        if not isinstance(v, datetime):
            raise ValueError("Field must be a valid datetime object")
        return v.isoformat()
    
    class Config:
        from_attributes = True
        
class EditUserProfile(BaseModel):
    full_name: Optional[str]
    gender: Optional[Gender]
    birth_date: Optional[datetime]
    phone_number: Optional[str]
    address: Optional[str]
    profile_picture: Optional[UploadFile]
    
    
    @field_validator("full_name", mode="before")
    def validate_full_name(cls, v):
        if not v:
            return None
        if v and v.strip() == "":
            raise ValueError("Full name must not be empty")
        return v
    
    @field_validator("phone_number", mode="before")
    def validate_phone_number(cls, v):
        if not v:
            return None
        if v and not v.isdigit():
            raise ValueError("Phone number must be a valid phone number")
        return v
    
    @field_validator("gender", mode="before")
    def validate_gender(cls, v):
        if not v:
            return None
        if v and not isinstance(v, Gender):
            raise ValueError("Gender must be a valid Gender enum")
        return v

    @field_validator("profile_picture", mode="before")
    def validate_image(cls, v):
        if not v:
            return None
        if v and not v.size < 5 * 1024 * 1024:
            raise ValueError("Image must be less than 5MB")
        if v and not v.filename.endswith(('.jpg', '.jpeg', '.png')):
            raise ValueError("Image must be a valid image format")
        return v

    @field_validator("birth_date", mode="before")
    def validate_datetime_fields(cls, v):
        if not v:
            return None
        if not isinstance(v, datetime):
            raise ValueError("Field must be a valid datetime object")
        return v.isoformat()
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()  # Menggunakan format ISO 8601
        }