from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from datetime import datetime
from uuid import uuid4, UUID
from typing import List, Dict, Any, Optional

class Role(Enum):
    ADMIN = "Admin"
    USER = "User"
    EO = "Event Organizer"
    
    def __str__(self):
        return self.value

class UserStatus(Enum):
    BASIC = "Basic"
    PREMIUM = "Premium"
    
    def __str__(self):
        return self.value
    

class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"
    
    def __str__(self):
        return self.value

class User(SQLModel, table=True):
    __tablename__ = 'users'

    user_id: UUID = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    full_name: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True)
    gender: Gender = Field(nullable=True)
    birth_date: datetime = Field(default=None, nullable=True)
    phone_number: str = Field(default=None, max_length=16, nullable=True)
    nik: str = Field(default=None, max_length=16, nullable=True)
    address: str = Field(default=None, max_length=100, nullable=True)
    role: Role = Field(default=Role.USER)
    status: UserStatus = Field(default=UserStatus.BASIC,)
    password_hash: str = Field(nullable=False, max_length=255)
    
    profile_picture: str = Field(default=None, nullable=True)
    email_verified_at: datetime = Field(default=None, nullable=True)
    
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False, sa_column_kwargs={"onupdate": datetime.now})
    
    # Foreign Keys
    code_province: str = Field(foreign_key="provinces.code_province", nullable=True)  # FK ke provinces
    code_city: str = Field(foreign_key="cities.code_city", nullable=True)  # FK ke cities
    code_district: str = Field(foreign_key="districts.code_district", nullable=True) # FK ke districts
    code_village: str = Field(foreign_key="villages.code_village", nullable=True)  # FK ke villages

    # Relationships
    province: "Province" = Relationship(back_populates="users")
    city: "City" = Relationship(back_populates="users")
    district: "District" = Relationship(back_populates="users")
    village: "Village" = Relationship(back_populates="users")
    
    
    # Relasi ke model Provider (One-to-Many)
    providers: List["Provider"] = Relationship(back_populates="user")
    otp: List["OTP"] = Relationship(back_populates="user")
    personal_access_tokens: List["PersonalAccessToken"] = Relationship(back_populates="user")
    # One-to-One Relationship
    organizer: Optional["EventOrganizer"] = Relationship(back_populates="user")
    
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