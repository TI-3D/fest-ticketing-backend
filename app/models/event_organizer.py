from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4
from enum import Enum
from datetime import datetime
from typing import List

# Enum for Organizer Status
class OrganizerStatus(str, Enum):
    PENDING = "Pending"
    ACTIVE = "Active"
    INACTIVE = "Inactive"

# Event Organizer Model
class EventOrganizer(SQLModel, table=True):
    __tablename__ = "eventorganizers"

    organizer_id: UUID = Field(default_factory=uuid4, primary_key=True)
    company_name: str
    company_address: str
    status: OrganizerStatus = Field(default=OrganizerStatus.PENDING)
    user_id: UUID = Field(foreign_key="users.user_id")
    verified_at: datetime = Field(default=None)

    # Foreign Keys
    code_province: str = Field(foreign_key="provinces.code_province")  # FK ke provinces
    code_city: str = Field(foreign_key="cities.code_city")  # FK ke cities
    code_district: str = Field(foreign_key="districts.code_district")  # FK ke districts
    code_village: str = Field(foreign_key="villages.code_village")  # FK ke villages

    # Relationships
    province: "Province" = Relationship(back_populates="organizers")
    city: "City" = Relationship(back_populates="organizers")
    district: "District" = Relationship(back_populates="organizers")
    village: "Village" = Relationship(back_populates="organizers")
    user: "User" = Relationship(back_populates="organizer")
    events: List["Event"] = Relationship(back_populates="organizer")
