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

    def __str__(self):
        return self.value


# Event Model
class Event(SQLModel, table=True):
    __tablename__ = "events"

    event_id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    description: str
    location: str
    status: EventStatus = Field(default=EventStatus.PENDING)

    # Foreign Keys
    organizer_id: UUID = Field(foreign_key="eventorganizers.organizer_id")
    code_province: str = Field(foreign_key="provinces.code_province")
    code_city: str = Field(foreign_key="cities.code_city")
    code_district: str = Field(foreign_key="districts.code_district")
    code_village: str = Field(foreign_key="villages.code_village")

    # Relationships
    province: "Province" = Relationship(back_populates="events")
    city: "City" = Relationship(back_populates="events")
    district: "District" = Relationship(back_populates="events")
    village: "Village" = Relationship(back_populates="events")
    schedules: List["Schedule"] = Relationship(back_populates="event")
    organizer: "EventOrganizer" = Relationship(back_populates="events")
    categories: List["EventCategories"] = Relationship(back_populates="events", link_model=EventCategoryAssociation)
    event_classes: List["EventClass"] = Relationship(back_populates="event")
    images: List["EventImage"] = Relationship(back_populates="event")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False, sa_column_kwargs={"onupdate": datetime.now})
    
    
