from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, Dict, Any
from uuid import UUID, uuid4
from decimal import Decimal

class EventClass(SQLModel, table=True):
    __tablename__ = "event_class"

    event_class_id: UUID = Field(default_factory=uuid4, primary_key=True)
    event_id: UUID = Field(foreign_key="events.event_id")
    class_name: str
    base_price: Decimal
    count: int
    description: Optional[str] = None

    event: "Event" = Relationship(back_populates="event_classes")
    
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
    
