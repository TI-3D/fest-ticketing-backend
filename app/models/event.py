from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum
from typing import List, Dict, Any
from app.models.event_category_association import EventCategoryAssociation


# Enum for Event Status
class EventStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"


# Event Model
class Event(SQLModel, table=True):
    __tablename__ = "events"

    event_id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    description: str
    location: str
    status: EventStatus = Field(default=EventStatus.PENDING)
    date: datetime
    image: str = Field(default=None, nullable=False)
    count_views: int = Field(default=0)

    # # Foreign Keys
    organizer_id: UUID = Field(foreign_key="eventorganizers.organizer_id")

    # Relationships
    organizer: "EventOrganizer" = Relationship(back_populates="events")
    categories: List["EventCategories"] = Relationship(back_populates="events", link_model=EventCategoryAssociation)
    event_classes: List["EventClass"] = Relationship(back_populates="event")
    payments: List["Payment"] = Relationship(back_populates="event")  # Relasi ke Payment
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False, sa_column_kwargs={"onupdate": datetime.now})
    
    
