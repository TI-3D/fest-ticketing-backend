from sqlmodel import Field, SQLModel, Relationship
from typing import List, Dict, Any
from app.models.event_category_association import EventCategoryAssociation


class EventCategories(SQLModel, table=True):
    __tablename__ = 'event_categories'

    category_name: str = Field(primary_key=True)

    # Relationships
    events: List["Event"] = Relationship(back_populates="categories", link_model=EventCategoryAssociation)
