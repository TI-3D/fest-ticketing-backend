from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from app.models.user import User
from uuid import UUID


# Enum to represent the provider names
class ProviderName(Enum):
    EMAIL = "Email"
    GOOGLE = "Google"
    FACEBOOK = "Facebook"
    TWITTER = "Twitter"

    def __str__(self):
        return self.value


# Provider Model
class Provider(SQLModel, table=True):
    __tablename__ = 'providers'

    provider_id: int = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="users.user_id", nullable=False)
    provider_name: ProviderName = Field(nullable=False)
    external_provider_id: str = Field(nullable=True)

    # Relationship to User
    user: "User" = Relationship(back_populates="providers")