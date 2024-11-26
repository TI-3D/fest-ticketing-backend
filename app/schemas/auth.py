from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, Dict, Any
from app.models.user import Gender, User
from app.schemas.response import ResponseModel, ResponseSuccess


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


class TokenData(BaseModel):
    token: str
    token_type: str
    expires_in: int

class TokenPair(BaseModel):
    access_token: TokenData
    
class SignupResponse(ResponseSuccess):
    data: Dict[str, str]
    

class SigninResponse(ResponseSuccess):
    token: TokenPair