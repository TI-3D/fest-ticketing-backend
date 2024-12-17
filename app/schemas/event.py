from uuid import UUID
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, field_validator
from app.models import EventStatus, EventOrganizer, EventCategories, EventClass
from app.schemas.response import ResponseSuccess
from fastapi import UploadFile


class EventClassBase(BaseModel):
    event_class_id: UUID
    event_id: UUID
    class_name: str
    base_price: float
    count: int
    description: Optional[str] = None

    @field_validator("event_class_id", "event_id", mode="before")
    def validate_id(cls, v):
        if not isinstance(v, UUID):
            raise ValueError("Invalid UUID")
        return str(v)

    @field_validator("base_price")
    def validate_base_price(cls, v):
        if not isinstance(v, float):
            raise ValueError("Invalid base price")
        return v

    class Config:
        from_attributes = True

class EventBase(BaseModel):
    event_id: UUID
    name: str
    description: str
    location: str
    status: str
    date: datetime

    organizer: Optional[EventOrganizer]
    categories: List[str]
    event_classes: List[EventClass]
    image: str

    created_at: datetime
    updated_at: datetime
    
    @field_validator("date", mode="before")
    def validate_date(cls, v):
        if not isinstance(v, datetime):
            raise ValueError("Invalid date")
        return v.isoformat()
    
    @field_validator("image", mode="before")
    def validate_image(cls, v):
        if not isinstance(v, str):
            raise ValueError("Invalid image")
        return v
    
    @field_validator("categories", mode="before")
    def validate_categories(cls, v):
        if not all(isinstance(item, EventCategories) for item in v):
            raise ValueError("Invalid categories")
        return [item.category_name for item in v]
    
    @field_validator("event_classes", mode="before")
    def validate_event_classes(cls, v):
        if not all(isinstance(item, EventClass) for item in v):
            raise ValueError("Invalid event classes")
        return [EventClassBase.model_validate(item) for item in v]

    @field_validator("event_id", mode="before")
    def validate_id(cls, v):
        if not isinstance(v, UUID):
            raise ValueError("Invalid UUID")
        return str(v)

    @field_validator("status", mode="before")
    def validate_status(cls, v):
        if not isinstance(v, EventStatus):
            raise ValueError("Invalid status")
        return v.value  # Return the string value of the Enum

    @field_validator("organizer")
    def validate_organizer(cls, v):
        if v and not isinstance(v, EventOrganizer):
            raise ValueError("Invalid organizer")
        return v

    @field_validator("created_at", "updated_at")
    def validate_date(cls, v):
        if not isinstance(v, datetime):
            raise ValueError("Invalid date")
        return v

    class Config:
        from_attributes = True

class EventResponse(ResponseSuccess):
    data: List[EventBase]

    @field_validator("data")
    def validate_data(cls, v):
        if not all(isinstance(item, EventBase) for item in v):
            raise ValueError("Invalid data, each item must be of type EventBase")
        return [EventBase.model_validate(item) for item in v]

    class Config:
        from_attributes = True

class EventClassCreate(BaseModel):
    class_name: str
    base_price: float
    count: int
    description: Optional[str] = None

    @field_validator("base_price")
    def validate_base_price(cls, v):
        if not isinstance(v, float):
            raise ValueError("Invalid base price")
        return v

    class Config:
        from_attributes = True
        
class EventCreate(BaseModel):
    name: str
    description: str
    location: str
    categories: List[str]
    date: datetime
    event_classes: List[EventClassCreate]
    image: UploadFile
    
    @field_validator("date", mode="before")
    def validate_date(cls, v):
        if not isinstance(v, datetime):
            raise ValueError("Invalid date")
        return v.isoformat()

    @field_validator("categories", mode="before")
    def validate_categories(cls, v):
        if not all(isinstance(item, str) for item in v):
            raise ValueError("Invalid categories")
        return v
    
    @field_validator("image", mode="before")
    def validate_image(cls, v):
        if v and not v.size < 5 * 1024 * 1024:
            raise ValueError("Image must be less than 5MB")
        if v and not v.filename.endswith(('.jpg', '.jpeg', '.png')):
            raise ValueError("Image must be a valid image format")
        return v

    @field_validator("event_classes", mode="before")
    def validate_event_classes(cls, v):
        if not all(isinstance(item, EventClassCreate) for item in v):
            raise ValueError("Invalid event classes")
        return [EventClassCreate.model_validate(item) for item in v]

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()  # Menggunakan format ISO 8601
        }

class EventUpdate(BaseModel):
    event_id: str
    name: str
    description: str
    location: str
    categories: List[str]
    date: datetime
    event_classes: List[EventClassCreate]
    image: Optional[UploadFile] = None
    
    @field_validator("event_id", mode="before")
    def validate_id(cls, v):
        if not isinstance(v, str):
            raise ValueError("Invalid UUID")
        return v
        
    
    @field_validator("date", mode="before")
    def validate_date(cls, v):
        if not isinstance(v, datetime):
            raise ValueError("Invalid date")
        return v.isoformat()

    @field_validator("categories", mode="before")
    def validate_categories(cls, v):
        if not all(isinstance(item, str) for item in v):
            raise ValueError("Invalid categories")
        return v
    
    @field_validator("image", mode="before")
    def validate_image(cls, v):
        if not v:
            return None
        if v and not v.size < 5 * 1024 * 1024:
            raise ValueError("Image must be less than 5MB")
        if v and not v.filename.endswith(('.jpg', '.jpeg', '.png')):
            raise ValueError("Image must be a valid image format")
        return v

    @field_validator("event_classes", mode="before")
    def validate_event_classes(cls, v):
        if not all(isinstance(item, EventClassCreate) for item in v):     
            raise ValueError("Invalid event classes")   
        return [EventClassCreate.model_validate(item) for item in v]
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()  # Menggunakan format ISO 8601
        }
        
        
class ChangeEventStatus(BaseModel):
    status: EventStatus
    
    @field_validator('status')
    def validate_status(cls, v):
        if not isinstance(v, EventStatus):
            raise ValueError("Status must be an instance of EventStatus Enum")
        return v
