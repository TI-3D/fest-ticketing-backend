from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from app.models.user import User
from uuid import UUID
from typing import Dict, Any

class ProviderName(Enum):
    EMAIL = "Email"
    GOOGLE = "Google"
    FACEBOOK = "Facebook"
    TWITTER = "Twitter"
    
    def __str__(self):
        return self.value
    
class Provider(SQLModel, table=True):
    __tablename__ = 'providers'

    provider_id: int = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="users.user_id", nullable=False)
    provider_name: ProviderName = Field(nullable=False)
    external_provider_id: str = Field(nullable=True)

    # Relationship ke User
    user: "User" = Relationship(back_populates="providers")
    
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