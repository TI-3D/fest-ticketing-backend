from pydantic import BaseModel
from typing import List

# Province Schema
class ProvinceBase(BaseModel):
    code_province: str
    name_province: str
    
    class Config:
        from_attributes = True

# City Schema
class CityBase(BaseModel):
    code_city: str
    name_city: str
    code_province: str  # Foreign key to Province
    
    class Config:
        from_attributes = True    

# District Schema
class DistrictBase(BaseModel):
    code_district: str
    name_district: str
    code_city: str  # Foreign key to City
    
    class Config:
        from_attributes = True
        
# Village Schema
class VillageBase(BaseModel):
    code_village: str
    name_village: str
    code_district: str  # Foreign key to District
    
    class Config:
        from_attributes = True
