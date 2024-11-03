from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, Dict, Any
from beanie import PydanticObjectId
from app.models.user import Gender, User
from app.schemas.response import ResponseModel

class SignupRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    gender: Gender
    
    @field_validator('email')
    def validate_email(cls, value):
        if not value.strip():
            raise ValueError('Email cannot be empty')
        if len(value) > 255:
            raise ValueError('Email must be less than 255 characters')
        return value

    @field_validator('full_name')
    def validate_full_name(cls, value):
        if not value.strip():
            raise ValueError('Full name cannot be empty')
        if len(value) > 255:
            raise ValueError('Full name must be less than 255 characters')
        if not value.replace(' ', '').isalpha():
            raise ValueError('Full name must contain only alphabetic characters')
        return value

    @field_validator('password')
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return value
    
    @field_validator('gender')
    def validate_gender(cls, value):
        if value not in Gender.__members__.values():
            raise ValueError('Invalid gender value')

class SigninRequest(BaseModel):
    email: EmailStr
    password: str
    device_id: Optional[str] = None
    
    @field_validator('email')
    def validate_email(cls, value):
        if not value.strip():
            raise ValueError('Email cannot be empty')
        if len(value) > 255:
            raise ValueError('Email must be less than 255 characters')
        return value
    
    @field_validator('password')
    def validate_password(cls, value):
        if not value.strip():
            raise ValueError('Password cannot be empty')
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return value

class GoogleSignupRequest(BaseModel):
    google_id: str
    email: EmailStr
    full_name: Optional[str]

    @field_validator('google_id')
    def validate_google_id(cls, value):
        if not value.strip():
            raise ValueError('Google ID cannot be empty')
        if len(value) > 255:
            raise ValueError('Google ID must be less than 255 characters')
        return value
    
    @field_validator('full_name')
    def validate_full_name(cls, value):
        if value and len(value) > 255:
            raise ValueError('Full name must be less than 255 characters')
        return value
    
    @field_validator('email')
    def validate_email(cls, value):
        if not value.strip():
            raise ValueError('Email cannot be empty')
        if len(value) > 255:
            raise ValueError('Email must be less than 255 characters')
        return value

class GoogleSigninRequest(BaseModel):
    google_id: str

    @field_validator('google_id')
    def validate_google_id(cls, value):
        if not value.strip():
            raise ValueError('Google ID cannot be empty')
        if len(value) > 255:
            raise ValueError('Google ID must be less than 255 characters')
        return value

class TokenData(BaseModel):
    token: str
    token_type: str
    expires_in: int

class TokenPair(BaseModel):
    access_token: TokenData
    
class SignupResponse(ResponseModel):
    pass
    

class SigninResponse(ResponseModel):
    data: Dict[str, User]
    token: TokenPair