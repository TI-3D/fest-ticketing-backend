from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from datetime import datetime
from typing import Optional
from app.models import PaymentStatus, PaymentMethodType, User, Event, EventClass
from app.schemas.user import UserBase
from app.schemas.event import EventBase, EventClassBase

class PaymentRequest(BaseModel):
    amount: float
    qty: int
    total: float
    event_id: UUID
    event_class_id: UUID
    payment_method: PaymentMethodType  # Perbaiki nama field menjadi lowpercase

    @field_validator("event_id", "event_class_id", mode="before")
    def validate_uuid_fields(cls, v):
        if not isinstance(v, UUID):
            raise ValueError("Field must be a valid UUID")
        return v

    @field_validator("amount", "total", mode="before")
    def validate_amount_fields(cls, v):
        if not isinstance(v, float):
            raise ValueError("Field must be a valid float")
        if v < 0:
            raise ValueError("Field must be a non-negative float")
        return v

    @field_validator("qty", mode="before")
    def validate_qty(cls, v):
        if not isinstance(v, int) or v <= 0:
            raise ValueError("Field must be a positive integer")
        return v

    @field_validator("total", mode="before")
    def validate_total(cls, v, values):
    #     amount = values.get("amount")
    #     qty = values.get("qty")
    #     if amount is not None and qty is not None:
    #         expected_total = amount * qty
    #         if v != expected_total:
    #             raise ValueError(f"Total must be equal to amount * qty ({amount} * {qty})")
        return v

    @field_validator("payment_method", mode="before")
    def validate_payment_method(cls, v):
        if not isinstance(v, PaymentMethodType):
            raise ValueError("Field must be a valid PaymentMethodType")
        return v

class PaymentResponse(BaseModel):
    payment_id: UUID
    event_id: UUID
    event_class_id: UUID
    user_id: UUID
    amount: float
    qty: int
    date: datetime
    total: float
    payment_status: PaymentStatus
    payment_method: PaymentMethodType
    
    user: Optional[User]
    event: Optional[Event]
    event_class: Optional[EventClass]
    
    created_at: datetime
    updated_at: datetime
    
    @field_validator("payment_id", "event_id", "event_class_id", "user_id", mode="before")
    def validate_ids(cls, v):
        if not isinstance(v, UUID):
            raise ValueError("Field must be a valid UUID")
        return str(v)
    
    @field_validator("amount", "total", mode="before")
    def validate_amount_fields(cls, v):
        if not isinstance(v, float):
            raise ValueError("Field must be a valid float")
        if v < 0:
            raise ValueError("Field must be a non-negative float")
        return v

    @field_validator("qty", mode="before")
    def validate_qty(cls, v):
        if not isinstance(v, int) or v <= 0:
            raise ValueError("Field must be a positive integer")
        return v
    
    @field_validator("payment_method", mode="before")
    def validate_payment_method(cls, v):
        if not isinstance(v, PaymentMethodType):
            raise ValueError("Field must be a valid PaymentMethodType")
        return v

    @field_validator("total", mode="before")
    def validate_total(cls, v, values):
        # amount = values.get("amount")
        # qty = values.get("qty")
        # if amount is not None and qty is not None:
        #     expected_total = amount * qty
        #     if v != expected_total:
        #         raise ValueError(f"Total must be equal to amount * qty ({amount} * {qty})")
        return v
    
    @field_validator("payment_status", mode="before")
    def validate_payment_status(cls, v):
        if not isinstance(v, PaymentStatus):
            raise ValueError("Field must be a valid PaymentStatus") 
        return v
    
    @field_validator("created_at", "updated_at", mode="before")
    def validate_datetime_fields(cls, v):
        if not v:
            return None
        if not isinstance(v, datetime):
            raise ValueError("Field must be a valid datetime object")
        return v.isoformat()
    
    @field_validator("user", mode="before")
    def validate_user(cls, v):
        if not v:
            return None
        if v and not isinstance(v, User):
            raise ValueError("Invalid user classes")
        return v
    
    @field_validator("event", mode="before")
    def validate_event(cls, v):
        if not v:
            return None
        if v and not isinstance(v, Event):
            raise ValueError("Invalid event classes")
        return v
    
    @field_validator("event_class", mode="before")
    def validate_event_class(cls, v):
        if not v:
            return None
        if v and not isinstance(v, EventClass):
            raise ValueError("Invalid event classes")
        return v
        
    class Config:
        from_attributes = True

class PaymentStatusUpdate(BaseModel):
    payment_status: PaymentStatus
    
    @field_validator("payment_status", mode="before")
    def validate_payment_status(cls, v):
        if not isinstance(v, PaymentStatus):
            raise ValueError("Field must be a valid PaymentStatus")
        return v