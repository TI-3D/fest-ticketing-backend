from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID
from typing import Dict, Any

class PersonalAccessToken(SQLModel, table=True):
    __tablename__ = 'personal_access_tokens'

    token_id: Optional[int] = Field(default=None, primary_key=True)
    device_id: Optional[str] = Field(default=None)
    access_token: str = Field(index=True, nullable=False, unique=True)
    user_id: UUID = Field(foreign_key="users.user_id", nullable=False)
    created_at: datetime = Field(default=datetime.now)
    expires_at: datetime = Field(nullable=False)

    # Relationship to User
    user: "User" = Relationship(back_populates="personal_access_tokens")
    
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