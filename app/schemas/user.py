from uuid import UUID
from datetime import date, datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, EmailStr, field_validator
from app.models.user import Gender, Role, UserStatus

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    gender: Optional[Gender]
    birth_date: Optional[date]
    phone_number: Optional[str]
    NIK: Optional[str]
    address: Optional[str]
    role: Role = Role.USER
    status: UserStatus = UserStatus.BASIC

    @field_validator('full_name')
    def validate_full_name(cls, value):
        if not value.strip():
            raise ValueError('Full name cannot be empty')
        if len(value) > 255:
            raise ValueError('Full name must be less than 255 characters')
        if not value.replace(' ', '').isalpha():
            raise ValueError('Full name must contain only alphabetic characters')
        return value

    @field_validator('phone_number')
    def validate_phone_number(cls, value):
        if value and not value.isdigit():
            raise ValueError('Phone number must contain only digits')
        if value and len(value) > 16:
            raise ValueError('Phone number must be less than 16 characters')
        if value and len(value) < 10:
            raise ValueError('Phone number must be at least 10 characters')
        if value and not value.startswith('08'):
            raise ValueError('Phone number must start with +62')
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

class UserRead(BaseModel):
    user_id: UUID
    full_name: str
    email: EmailStr
    gender: Optional[Gender]
    birth_date: Optional[date]
    phone_number: Optional[str]
    NIK: Optional[str]
    address: Optional[str]
    role: Role
    status: UserStatus
    created_at: datetime
    updated_at: datetime

class UserUpdate(BaseModel):
    full_name: Optional[str]
    email: Optional[EmailStr]
    gender: Optional[Gender]
    birth_date: Optional[date]
    phone_number: Optional[str]
    NIK: Optional[str]
    address: Optional[str]
    role: Optional[Role]    
    status: Optional[UserStatus]

    @field_validator('full_name')
    def validate_full_name(cls, value):
        if not value.strip():
            raise ValueError('Full name cannot be empty')
        if len(value) > 255:
            raise ValueError('Full name must be less than 255 characters')
        if not value.replace(' ', '').isalpha():
            raise ValueError('Full name must contain only alphabetic characters')
        return value

    @field_validator('phone_number')
    def validate_phone_number(cls, value):
        if value and not value.isdigit():
            raise ValueError('Phone number must contain only digits')
        if value and len(value) > 16:
            raise ValueError('Phone number must be less than 16 characters')
        if value and len(value) < 10:
            raise ValueError('Phone number must be at least 10 characters')
        if value and not value.startswith('08'):
            raise ValueError('Phone number must start with +62')
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