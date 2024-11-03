from beanie import Document, PydanticObjectId
from pydantic import Field, field_validator
from typing import Optional
from datetime import datetime, timedelta

class PersonalAccessToken(Document):
    personal_access_token_id: PydanticObjectId = Field(default_factory=PydanticObjectId, primary_key=True)
    user_id: PydanticObjectId = Field(default_factory=PydanticObjectId)
    device_id: Optional[str] = Field(default=None)
    is_google: bool = Field(default=False)
    access_token: str 
    access_token_expired: datetime
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    

    @field_validator("access_token", mode="before")
    def validate_token(cls, token: str) -> str:
        if not token:
            raise ValueError("Token must not be empty.")
        if len(token) < 10:
            raise ValueError("Token must be at least 10 characters long.")
        return token

    # Validator for expiration dates
    @field_validator("access_token_expired", mode="before")
    def validate_expiration_dates(cls, expiration: datetime) -> datetime:
        if expiration < datetime.now():
            raise ValueError("Expiration date must be in the future.")
        return expiration


    # Example validator for user_id
    @field_validator("user_id", mode="before")
    def validate_user_id(cls, user_id: PydanticObjectId) -> PydanticObjectId:
        if not user_id:
            raise ValueError("User ID must not be empty.")
        return user_id
    
    class Settings:
        collection = "personal_access_tokens"
