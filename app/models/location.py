from sqlmodel import SQLModel, Field, Relationship
from typing import List, Dict, Any

# Province Model
class Province(SQLModel, table=True):
    __tablename__ = "provinces"

    code_province: str = Field(primary_key=True)
    name_province: str
    cities: List["City"] = Relationship(back_populates="province")
    users: List["User"] = Relationship(back_populates="province")  # back_populates should match 'province' in User
    organizers: List["EventOrganizer"] = Relationship(back_populates="province")
    events: List["Event"] = Relationship(back_populates="province") 

# City Model
class City(SQLModel, table=True):
    __tablename__ = "cities"

    code_city: str = Field(primary_key=True) 
    name_city: str
    code_province: str = Field(foreign_key="provinces.code_province")
    province: Province = Relationship(back_populates="cities")
    districts: List["District"] = Relationship(back_populates="city")
    users: List["User"] = Relationship(back_populates="city")  # back_populates should match 'city' in User
    organizers: List["EventOrganizer"] = Relationship(back_populates="city")
    events: List["Event"] = Relationship(back_populates="city")  # back_populates should match 'city' in Event
    
class District(SQLModel, table=True):
    __tablename__ = "districts"

    code_district: str = Field(primary_key=True) 
    name_district: str
    code_city: str = Field(foreign_key="cities.code_city")
    city: City = Relationship(back_populates="districts")
    villages: List["Village"] = Relationship(back_populates="district")
    users: List["User"] = Relationship(back_populates="district")  # back_populates should match 'district' in User
    organizers: List["EventOrganizer"] = Relationship(back_populates="district")
    events: List["Event"] = Relationship(back_populates="district")  # back_populates should match 'district' in Event
    
# Village Model
class Village(SQLModel, table=True):
    __tablename__ = "villages"

    code_village: str = Field(primary_key=True)  # Menggunakan `code_village` sebagai primary key
    name_village: str
    code_district: str = Field(foreign_key="districts.code_district")
    district: District = Relationship(back_populates="villages")
    users: List["User"] = Relationship(back_populates="village")  # back_populates should match 'village' in User
    organizers: List["EventOrganizer"] = Relationship(back_populates="village")
    events: List["Event"] = Relationship(back_populates="village")  # back_populates should match 'village' in Event
    