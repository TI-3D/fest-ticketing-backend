from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from uuid import UUID

class OTP(SQLModel, table=True):
    __tablename__ = 'otps'

    otp_id: Optional[int] = Field(default=None, primary_key=True)
    otp_code: str = Field(index=True, nullable=False)
    user_id: UUID = Field(foreign_key="users.user_id", nullable=False)
    hashed_otp: str = Field(nullable=False)
    created_at: datetime = Field(default=datetime.now)
    expires_at: datetime = Field(nullable=False)

    # Relationship to User
    user: "User" = Relationship(back_populates="otp")