from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4
from datetime import datetime
from typing import Dict, Any


# Event Image Model
class EventImage(SQLModel, table=True):
    __tablename__ = "event_images"

    image_id: UUID = Field(default_factory=uuid4, primary_key=True)
    event_id: UUID = Field(foreign_key="events.event_id")
    image_url: str

    # Relationship to Event
    event: "Event" = Relationship(back_populates="images")