from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum
from typing import List, Optional

# Enum for Payment Status
class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    
# Enum for Payment Method Type
class PaymentMethodType(str, Enum):
    CREDIT_CARD = "CREDIT_CARD"
    GOPAY = "GOPAY"
    DANA = "DANA"
    OVO = "OVO"

# Payment Model
class Payment(SQLModel, table=True):
    __tablename__ = "payments"

    payment_id: UUID = Field(default_factory=uuid4, primary_key=True)
    amount: float
    qty: int
    total: float
    date: datetime = Field(default_factory=datetime.now)
    payment_status: PaymentStatus = Field(default=PaymentStatus.PENDING)
    payment_method: PaymentMethodType = Field(nullable=False)
    barcode: Optional[str] = Field(default=None, nullable=True)

    # Foreign Keys
    user_id: UUID = Field(foreign_key="users.user_id")
    event_id: UUID = Field(foreign_key="events.event_id")
    event_class_id: UUID = Field(foreign_key="event_classes.event_class_id")  # Pastikan nama tabel sesuai

    # Relationships
    user: "User" = Relationship(back_populates="payments")
    event: "Event" = Relationship(back_populates="payments")
    event_class: "EventClass" = Relationship(back_populates="payments")
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False, sa_column_kwargs={"onupdate": datetime.now})
