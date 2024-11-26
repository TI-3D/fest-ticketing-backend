from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4
from decimal import Decimal
from datetime import datetime
from typing import Optional, Dict, Any


# Event Class Model
class EventClass(SQLModel, table=True):
    __tablename__ = "event_class"

    event_class_id: UUID = Field(default_factory=uuid4, primary_key=True)
    event_id: UUID = Field(foreign_key="events.event_id")
    class_name: str
    base_price: Decimal
    count: int
    description: Optional[str] = None

    # Relationship to Event
    event: "Event" = Relationship(back_populates="event_classes")
