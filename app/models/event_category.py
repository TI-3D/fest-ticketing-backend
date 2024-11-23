from sqlmodel import Field, SQLModel
from typing import List, Dict, Any
from sqlmodel import Relationship
from app.models.event_category_association import EventCategoryAssociation

class EventCategories(SQLModel, table=True):
    __tablename__ = 'event_categories'
    category_name: str = Field(primary_key=True)
    
    events: List["Event"] = Relationship(back_populates="categories", link_model=EventCategoryAssociation)
    
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