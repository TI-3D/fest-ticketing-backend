from sqlmodel import SQLModel, Field, Relationship
from typing import List, Dict, Any
from uuid import uuid4, UUID
from datetime import datetime
from enum import Enum


# Enum to represent the days of the week
class DayOfWeek(str, Enum):
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"
    Sunday = "Sunday"

    def __str__(self):
        return self.value


# Schedule Model
class Schedule(SQLModel, table=True):
    __tablename__ = 'schedules'

    # Fields
    schedule_id: UUID = Field(default_factory=uuid4, primary_key=True)
    event_id: UUID = Field(foreign_key="events.event_id")
    day_of_week: DayOfWeek  # Day of the week, using the DayOfWeek enum
    date: datetime  # Specific date for the event
    start_time: datetime  # Start time of the event
    end_time: datetime  # End time of the event

    # Relationship with Event model
    event: "Event" = Relationship(back_populates="schedules")
