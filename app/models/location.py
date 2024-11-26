from sqlmodel import SQLModel, Field, Relationship
from typing import List, Dict, Any

# Province Model
class Province(SQLModel, table=True):
    __tablename__ = "provinces"

    code_province: str = Field(primary_key=True)
    name_province: str
    cities: List["City"] = Relationship(back_populates="province")
    organizers: List["EventOrganizer"] = Relationship(back_populates="province")
    events: List["Event"] = Relationship(back_populates="province") 
    users: List["User"] = Relationship(back_populates="province")  # back_populates should match 'province' in User
    
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

# City Model
class City(SQLModel, table=True):
    __tablename__ = "cities"

    code_city: str = Field(primary_key=True) 
    name_city: str
    code_province: str = Field(foreign_key="provinces.code_province")
    province: Province = Relationship(back_populates="cities")
    districts: List["District"] = Relationship(back_populates="city")
    organizers: List["EventOrganizer"] = Relationship(back_populates="city")
    events: List["Event"] = Relationship(back_populates="city")  # back_populates should match 'city' in Event
    users: List["User"] = Relationship(back_populates="city")  # back_populates should match 'city' in User
    
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

# District Model
class District(SQLModel, table=True):
    __tablename__ = "districts"

    code_district: str = Field(primary_key=True) 
    name_district: str
    code_city: str = Field(foreign_key="cities.code_city")
    city: City = Relationship(back_populates="districts")
    villages: List["Village"] = Relationship(back_populates="district")
    organizers: List["EventOrganizer"] = Relationship(back_populates="district")
    events: List["Event"] = Relationship(back_populates="district")  # back_populates should match 'district' in Event
    users: List["User"] = Relationship(back_populates="district")  # back_populates should match 'district' in User
    
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

# Village Model
class Village(SQLModel, table=True):
    __tablename__ = "villages"

    code_village: str = Field(primary_key=True)  # Menggunakan `code_village` sebagai primary key
    name_village: str
    code_district: str = Field(foreign_key="districts.code_district")
    district: District = Relationship(back_populates="villages")
    organizers: List["EventOrganizer"] = Relationship(back_populates="village")
    events: List["Event"] = Relationship(back_populates="village")  # back_populates should match 'village' in Event
    users: List["User"] = Relationship(back_populates="village")  # back_populates should match 'village' in User
    
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