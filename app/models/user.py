from beanie import Document,PydanticObjectId
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime, date
from enum import Enum

class Role(str, Enum):
    ADMIN = "Admin"
    USER = "User"
    EO = "Event Organizer"

class UserStatus(str, Enum):
    BASIC = "Basic"
    PREMIUM = "Premium"

class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"

class User(Document):
    user_id: PydanticObjectId = Field(default_factory=PydanticObjectId, primary_key=True)
    full_name: Optional[str] = Field(..., description="Full name of the user", required=True)
    email: EmailStr = Field(..., description="Email address of the user", required=True)
    gender: Optional[Gender] = None  
    birth_date: Optional[datetime] = None
    phone_number: Optional[str] = Field(None, max_length=16, description="Phone number must be 16 characters or less")
    NIK: Optional[str] = Field(None, max_length=16, description="NIK must be 16 characters")
    address: Optional[str] = Field(None, max_length=100, description="Address must be less than 100 characters")
    role: Role = Field(default=Role.USER)
    status: UserStatus = Field(default=UserStatus.BASIC)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @field_validator('full_name')
    def validate_full_name(cls, value):
        if not value:
            raise ValueError('Full name is required')
        if len(value) < 3:
            raise ValueError('Full name must be at least 3 characters')
        return value    
    
    @field_validator('email')
    def validate_email(cls, value):
        if not value:
            raise ValueError('Email is required')
        return value
        
    @field_validator('phone_number')
    def validate_phone_number(cls, value):
        if value and not value.isdigit():
            raise ValueError('Phone number must contain only digits')
        if value and len(value) > 16:
            raise ValueError('Phone number must be less than 16 characters')
        if value and len(value) < 10:
            raise ValueError('Phone number must be at least 10 characters')
        if value and not value.startswith("08"):
            raise ValueError('Phone number must start with 08')
        return value

    @field_validator('NIK')
    def validate_nik(cls, value):
        if value and not value.isdigit():
            raise ValueError('NIK must contain only digits')
        if value and len(value) != 16:
            raise ValueError('NIK must be 16 characters')
        return value

    @field_validator('address')
    def validate_address(cls, value):
        if value and len(value) > 100:
            raise ValueError('Address must be less than 100 characters')
        return value

    class Settings:
        collection = "users"
