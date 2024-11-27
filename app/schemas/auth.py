from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import Optional, Dict, Any
from app.models import Gender, User
from app.schemas.response import ResponseSuccess
from datetime import datetime
class SignupRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    confirm_password: str
    gender: Gender
    birth_date: datetime
    phone_number: str
    nik: str
    address: str
    profile_picture: Optional[str] = None
    code_province: str
    code_city: str
    code_district: str
    code_village: str
    
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
        confirm_password = values.get('confirm_password')

        if password != confirm_password:
            raise ValueError("Passwords do not match")

        return values

    @field_validator('gender')
    def validate_gender(cls, v):
        if v not in [Gender.MALE, Gender.FEMALE]:
            raise ValueError("Gender must be either 'Male' or 'Female'")
        return v

    @field_validator('phone_number')
    def validate_phone_number(cls, v):
        if len(v) < 10 or len(v) > 15:
            raise ValueError("Phone number must be between 10 and 15 digits")
        return v

    @field_validator('nik')
    def validate_nik(cls, v):
        if len(v) != 16:
            raise ValueError("NIK must be 16 digits long")
        return v

    @field_validator('address')
    def validate_address(cls, v):
        if not v.strip():
            raise ValueError("Address cannot be empty")
        if len(v) > 255:
            raise ValueError("Address must be less than 255 characters")
        return v
    
    @field_validator('code_province')
    def validate_code_province(cls, v):
        if len(v) != 2:
            raise ValueError("Province code must be 2 characters long")
        return v
    
    @field_validator('code_city')
    def validate_code_city(cls, v):
        if len(v) != 5:
            raise ValueError("City code must be 4 characters long")
        return v
    
    @field_validator('code_district')
    def validate_code_district(cls, v):
        if len(v) != 8:
            raise ValueError("District code must be 8 characters long")
        return v
    
    @field_validator('code_village')
    def validate_code_village(cls, v):
        if len(v) != 13:
            raise ValueError("Village code must be 13 characters long")
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