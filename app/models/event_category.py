from sqlmodel import Field, SQLModel
from typing import List
from sqlmodel import Relationship
from app.models.event_category_association import EventCategoryAssociation

class EventCategories(SQLModel, table=True):
    __tablename__ = 'event_categories'
    category_name: str = Field(primary_key=True)
    
    events: List["Event"] = Relationship(back_populates="categories", link_model=EventCategoryAssociation)