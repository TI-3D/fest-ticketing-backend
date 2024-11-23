from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum
from typing import List, Dict, Any
from app.models.event_category_association import EventCategoryAssociation

class EventStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"
    
    def __str__(self):
        return self.value

class Event(SQLModel, table=True):
    __tablename__ = "events"

    event_id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    description: str
    location: str
    status: EventStatus = Field(default=EventStatus.PENDING)

    # Foreign Keys
    organizer_id: UUID = Field(foreign_key="eventorganizers.organizer_id")
    code_province: str = Field(foreign_key="provinces.code_province")  # FK ke provinces
    code_city: str = Field(foreign_key="cities.code_city")  # FK ke cities
    code_district: str = Field(foreign_key="districts.code_district") # FK ke districts
    code_village: str = Field(foreign_key="villages.code_village")  # FK ke villages

    # Relationships
    province: "Province" = Relationship(back_populates="events")  # back_populates should match 'events' in Province
    city: "City" = Relationship(back_populates="events")  # back_populates should match 'events' in City
    district: "District" = Relationship(back_populates="events")  # back_populates should match 'events' in District
    village: "Village" = Relationship(back_populates="events")  # back_populates should match 'events' in Village

    schedules: List["Schedule"] = Relationship(back_populates="event")
    organizer: "EventOrganizer" = Relationship(back_populates="events")
    
    categories: List["EventCategories"] = Relationship(
        back_populates="events", link_model=EventCategoryAssociation
    )
    event_classes: List["EventClass"] = Relationship(back_populates="event")
    images: List["EventImage"] = Relationship(back_populates="event")
    
    def model_dump(self, *args, **kwargs) -> Dict[str, Any]:
        data = super().model_dump(*args, **kwargs)  # Use dict() as an alternative for serialization
        # Convert datetime fields to string
        for field, value in data.items():
            if isinstance(value, datetime):
                # Convert datetime to ISO 8601 string format
                data[field] = value.isoformat()
            elif isinstance(value, Enum):
                # Convert Enum to string
                data[field] = str(value)
            elif isinstance(value, UUID):
                # Convert UUID to string
                data[field] = str(value)
        return data
