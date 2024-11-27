from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
from app.models import Gender, Role
from datetime import datetime
class UserBase(BaseModel):
    user_id: str
    full_name: str
    email: EmailStr
    gender: Optional[str] = None
    birth_date: str
    phone_number: str
    nik: str
    address: str
    role: str
    profile_picture: Optional[str] = None
    code_province: str
    code_city: str
    code_district: str
    code_village: str
    created_at: str
    updated_at: str
    
    @field_validator("gender", mode="before")
    def validate_gender(cls, v):
        if isinstance(v, Gender):
            return str(v)
        return v
    
    @field_validator("role", mode="before")
    def validate_role(cls, v):
        if isinstance(v, Role):
            return str(v)
        return v
    
    @field_validator("user_id", mode="before")
    def validate_user_id(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v

    @field_validator("birth_date", "created_at", "updated_at", mode="before")
    def validate_datetime_fields(cls, v):
        if isinstance(v, datetime):
            return v.isoformat()  
        return v
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    gender: Optional[str] = None
    birth_date: Optional[str] = None
    phone_number: Optional[str] = None
    nik: Optional[str] = None
    address: Optional[str] = None
    profile_picture: Optional[str] = None
    
    class Config:
        from_attributes = True