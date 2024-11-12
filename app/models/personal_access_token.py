from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship


class PersonalAccessToken(SQLModel, table=True):
    __tablename__ = 'personal_access_tokens'

    token_id: Optional[int] = Field(default=None, primary_key=True)
    device_id: Optional[str] = Field(default=None)
    access_token: str = Field(index=True, nullable=False, unique=True)
    user_id: str = Field(foreign_key="users.user_id", nullable=False)
    created_at: datetime = Field(default=datetime.now)
    expires_at: datetime = Field(nullable=False)

    # Relationship to User
    user: "User" = Relationship(back_populates="personal_access_tokens")