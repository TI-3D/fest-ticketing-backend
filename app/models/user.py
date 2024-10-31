from beanie import Document
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from uuid import UUID, uuid4
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
    user_id: UUID = Field(default_factory=uuid4)
    full_name: str = Field(max_length=255, description="Full name of the user")
    email: EmailStr
    gender: Optional[Gender] = None  
    birth_date: Optional[date] = None
    phone_number: Optional[str] = Field(None, max_length=16, description="Phone number must be 16 characters or less")
    NIK: Optional[str] = Field(None, max_length=16, description="NIK must be 16 characters")
    address: Optional[str] = Field(None, max_length=100, description="Address must be less than 100 characters")
    role: Role = Field(default=Role.USER)
    status: UserStatus = Field(default=UserStatus.BASIC)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @validator('full_name')
    def validate_full_name(cls, value):
        if not value.strip():
            raise ValueError('Full name cannot be empty')
        if len(value) > 255:
            raise ValueError('Full name must be less than 255 characters')
        if not value.replace(' ', '').isalpha():
            raise ValueError('Full name must contain only alphabetic characters')
        return value

    @validator('phone_number')
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

    @validator('NIK')
    def validate_nik(cls, value):
        if value and not value.isdigit():
            raise ValueError('NIK must contain only digits')
        if value and len(value) != 16:
            raise ValueError('NIK must be 16 characters')
        return value

    @validator('address')
    def validate_address(cls, value):
        if value and len(value) > 100:
            raise ValueError('Address must be less than 100 characters')
        return value

    class Settings:
        collection = "users"
