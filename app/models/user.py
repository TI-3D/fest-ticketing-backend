from sqlmodel import Field, SQLModel, Relationship
from enum import Enum
from datetime import datetime
from uuid import uuid4, UUID
from typing import List, Optional

class Role(Enum):
    ADMIN = "Admin"
    USER = "User"
    EO = "EO"

class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"

class User(SQLModel, table=True):
    __tablename__ = 'users'

    user_id: UUID = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    full_name: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True)
    gender: Gender = Field(nullable=False)
    birth_date: datetime = Field(nullable=True)
    phone_number: str = Field(nullable=True, max_length=16)
    nik: str = Field(nullable=True, max_length=16, unique=True)
    address: str = Field(nullable=True, max_length=100)
    role: Role = Field(default=Role.USER)
    password_hash: str = Field(nullable=False, max_length=255)
    
    embedding: str = Field(default=None, nullable=True)
    profile_picture: str = Field(default=None, nullable=True)
    email_verified_at: datetime = Field(default=None, nullable=True)
    
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False, sa_column_kwargs={"onupdate": datetime.now})
    
    # Relationships
    providers: List["Provider"] = Relationship(back_populates="user")
    otp: List["OTP"] = Relationship(back_populates="user")
    personal_access_tokens: List["PersonalAccessToken"] = Relationship(back_populates="user")
    organizer: Optional["EventOrganizer"] = Relationship(back_populates="user")
    payments: List["Payment"] = Relationship(back_populates="user") # Relasi ke Payment