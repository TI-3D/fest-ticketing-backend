from beanie import Document, Link, PydanticObjectId
from pydantic import Field, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum
from app.models.user import User  # Ensure this import is below the class definition

class Provider(str, Enum):
    GOOGLE = "google"
    EMAIL = "email"

class Authentication(Document):
    authentication_id: Optional[PydanticObjectId] = Field(default_factory=PydanticObjectId, primary_key=True)
    provider: Provider = Field(description="Name of the authentication provider.")
    user: Link[User]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @field_validator('provider')
    def validate_provider(cls, value):
        if value not in Provider.__members__.values():
            raise ValueError('Invalid provider')
        return value

    class Settings:
        collection = "authentications"

class EmailAuthentication(Document):
    email_authentication_id: Optional[PydanticObjectId] = Field(default_factory=PydanticObjectId, primary_key=True)
    password: str = Field(..., min_length=3, max_length=255)
    user: Link[User]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @field_validator('password')
    def validate_password(cls, value):
        if len(value) < 3 or len(value) > 255:
            raise ValueError('Password must be between 3 and 255 characters')
        return value

    class Settings:
        collection = "email_authentications"

class GoogleAuthentication(Document):
    google_authentication_id: Optional[PydanticObjectId] = Field(default_factory=PydanticObjectId, primary_key=True)
    google_id: str = Field(..., min_length=3, max_length=255)
    user: Link[User]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @field_validator('google_id')
    def validate_google_id(cls, value):
        if len(value) < 3 or len(value) > 255:
            raise ValueError('Google ID must be between 3 and 255 characters')
        return value

    class Settings:
        collection = "google_authentications"