from sqlmodel import SQLModel, Field
from uuid import UUID
from datetime import datetime
from typing import Dict, Any

class EventCategoryAssociation(SQLModel, table=True):
    __tablename__ = 'event_category_association'

    event_id: UUID = Field(foreign_key="events.event_id", primary_key=True)
    category_name: str = Field(foreign_key="event_categories.category_name", primary_key=True)
    
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
