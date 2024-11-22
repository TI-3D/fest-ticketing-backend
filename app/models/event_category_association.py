from sqlmodel import SQLModel, Field
from uuid import UUID

class EventCategoryAssociation(SQLModel, table=True):
    __tablename__ = 'event_category_association'

    event_id: UUID = Field(foreign_key="events.event_id", primary_key=True)
    category_name: str = Field(foreign_key="event_categories.category_name", primary_key=True)
