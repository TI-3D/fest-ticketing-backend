from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Province, City, District, Village
from typing import List, Optional
from app.core.config import Logger
from sqlalchemy import select

class LocationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.logger = Logger(__name__).get_logger()  # Initialize the logger

    # Province
    async def get_provinces(self) -> Optional[List[Province]]:
        """
        Get all provinces from the database.
        """
        try:
            self.logger.info("Attempting to retrieve all provinces")
            result = await self.session.execute(select(Province))
            provinces = result.scalars().all()
            return provinces
        except Exception as e:
            self.logger.error(f"Error retrieving provinces: {str(e)}")
            raise

    async def get_province_by_code(self, code_province: str) -> Optional[Province]:
        """
        Get a province by its code.
        """
        try:
            result = await self.session.execute(select(Province).filter(Province.code_province == code_province))
            province = result.scalars().first()
            return province
        except Exception as e:
            self.logger.error(f"Error retrieving province by code {code_province}: {str(e)}")
            raise

    # City
    async def get_cities(self, province_code: str) -> List[City]:
        """
        Get all cities by province code.
        """
        try:
            result = await self.session.execute(select(City).filter(City.code_province == province_code))
            cities = result.scalars().all()
            return cities
        except Exception as e:
            self.logger.error(f"Error retrieving cities for province {province_code}: {str(e)}")
            raise

    async def get_city_by_code(self, code_city: str) -> Optional[City]:
        """
        Get a city by its code.
        """
        try:
            result = await self.session.execute(select(City).filter(City.code_city == code_city))
            city = result.scalars().first()
            return city
        except Exception as e:
            self.logger.error(f"Error retrieving city by code {code_city}: {str(e)}")
            raise

    # District
    async def get_districts(self, city_code: str) -> List[District]:
        """
        Get all districts by city code.
        """
        try:
            result = await self.session.execute(select(District).filter(District.code_city == city_code))
            districts = result.scalars().all()
            return districts
        except Exception as e:
            self.logger.error(f"Error retrieving districts for city {city_code}: {str(e)}")
            raise

    async def get_district_by_code(self, code_district: str) -> Optional[District]:
        """
        Get a district by its code.
        """
        try:
            result = await self.session.execute(select(District).filter(District.code_district == code_district))
            district = result.scalars().first()
            return district
        except Exception as e:
            self.logger.error(f"Error retrieving district by code {code_district}: {str(e)}")
            raise

    # Village
    async def get_villages(self, district_code: str) -> List[Village]:
        """
        Get all villages by district code.
        """
        try:
            result = await self.session.execute(select(Village).filter(Village.code_district == district_code))
            villages = result.scalars().all()
            return villages
        except Exception as e:
            self.logger.error(f"Error retrieving villages for district {district_code}: {str(e)}")
            raise

    async def get_village_by_code(self, code_village: str) -> Optional[Village]:
        """
        Get a village by its code.
        """
        try:
            result = await self.session.execute(select(Village).filter(Village.code_village == code_village))
            village = result.scalars().first()
            return village
        except Exception as e:
            self.logger.error(f"Error retrieving village by code {code_village}: {str(e)}")
            raise
