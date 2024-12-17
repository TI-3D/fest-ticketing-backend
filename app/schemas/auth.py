from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import Optional, Dict, Any
from app.models import Gender, User
from app.schemas.response import ResponseSuccess
from datetime import datetime
class SignupRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    password_confirmation: str
    gender: Gender
    
    @field_validator('full_name')
    def validate_full_name(cls, v):
        if not v.strip():
            raise ValueError("Full name cannot be empty")
        if len(v) > 255:
            raise ValueError("Full name must be less than 255 characters")
        return v
    
    @field_validator('email')
    def validate_email(cls, v):
        if not v.strip():
            raise ValueError("Email cannot be empty")
        if len(v) > 255:
            raise ValueError("Email must be less than 255 characters")
        return v

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v

    @model_validator(mode='before')
    def validate_password_match(cls, values):
        password = values.get('password')
        password_confirmation = values.get('password_confirmation')
        print(password, password_confirmation)
        print(len(password), type(password_confirmation))
        if password != password_confirmation:
            raise ValueError("Passwords do not match")

        return values

    @field_validator('gender')
    def validate_gender(cls, v):
        if not isinstance(v, Gender):
            raise ValueError("Gender must be either 'Male' or 'Female'")
        return v

    



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

class TokenClaim(BaseModel):
    sub: str
    exp: int = 0

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