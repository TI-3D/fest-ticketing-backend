from app.repositories import LocationRepository
from app.schemas.location import ProvinceBase, CityBase, DistrictBase, VillageBase
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from fastapi import HTTPException, status
from app.core.config import Logger

class LocationService:
    def __init__(self, session: AsyncSession):
        self.location_repository = LocationRepository(session)
        self.logger = Logger(__name__).get_logger()

    async def get_provinces(self) -> List[ProvinceBase]:
        """
        Get all provinces.
        """
        try:
            provinces = await self.location_repository.get_provinces()
            if not provinces:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No provinces found.")
            # Convert Province models to Pydantic schemas
            return [ProvinceBase.model_validate(province) for province in provinces]
        except HTTPException as e:
            self.logger.error(f"Error while retrieving provinces: {e}")
            raise e
        except Exception as e:
            self.logger.error(f"Error while retrieving provinces: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def get_province_by_code(self, code_province: str) -> ProvinceBase:
        """
        Get a province by its code.
        """
        try:
            province = await self.location_repository.get_province_by_code(code_province)
            if not province:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Province not found.")
            return ProvinceBase.model_validate(province)
        except HTTPException as e:
            self.logger.error(f"Error while retrieving province with code {code_province}: {e}")
            raise e
        except Exception as e:
            self.logger.error(f"Error while retrieving province with code {code_province}: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def get_cities_by_province(self, code_province: str) -> List[CityBase]:
        """
        Get all cities in a province.
        """
        try:
            cities = await self.location_repository.get_cities(code_province)
            if not cities:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No cities found for this province.")
            # Convert City models to Pydantic schemas
            return [CityBase.model_validate(city) for city in cities]
        except HTTPException as e:
            self.logger.error(f"Error while retrieving cities for province {code_province}: {e}")
            raise e            
        except Exception as e:
            self.logger.error(f"Error while retrieving cities for province {code_province}: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def get_city_by_code(self, code_city: str) -> CityBase:
        """
        Get a city by its code.
        """
        try:
            city = await self.location_repository.get_city_by_code(code_city)
            if not city:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found.")
            return CityBase.model_validate(city)
        except HTTPException as e:
            self.logger.error(f"Error while retrieving city with code {code_city}: {e}")
            raise e
        except Exception as e:
            self.logger.error(f"Error while retrieving city with code {code_city}: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def get_districts_by_city(self, code_city: str) -> List[DistrictBase]:
        """
        Get all districts in a city.
        """
        try:
            districts = await self.location_repository.get_districts(code_city)
            if not districts:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No districts found for this city.")
            # Convert District models to Pydantic schemas
            return [DistrictBase.model_validate(district) for district in districts]
        except HTTPException as e:
            self.logger.error(f"Error while retrieving districts for city {code_city}: {e}")
            raise e
        except Exception as e:
            self.logger.error(f"Error while retrieving districts for city {code_city}: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def get_district_by_code(self, code_district: str) -> DistrictBase:
        """
        Get a district by its code.
        """
        try:
            district = await self.location_repository.get_district_by_code(code_district)
            if not district:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="District not found.")
            return DistrictBase.model_validate(district)
        except HTTPException as e:
            self.logger.error(f"Error while retrieving district with code {code_district}: {e}")
            raise e
        except Exception as e:
            self.logger.error(f"Error while retrieving district with code {code_district}: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def get_villages_by_district(self, code_district: str) -> List[VillageBase]:
        """
        Get all villages in a district.
        """
        try:
            villages = await self.location_repository.get_villages(code_district)
            if not villages:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No villages found for this district.")
            # Convert Village models to Pydantic schemas
            return [VillageBase.model_validate(village) for village in villages]
        except HTTPException as e:
            self.logger.error(f"Error while retrieving villages for district {code_district}: {e}")
            raise e
        except Exception as e:
            self.logger.error(f"Error while retrieving villages for district {code_district}: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def get_village_by_code(self, code_village: str) -> VillageBase:
        """
        Get a village by its code.
        """
        try:
            village = await self.location_repository.get_village_by_code(code_village)
            if not village:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Village not found.")
            return VillageBase.model_validate(village)
        except HTTPException as e:
            self.logger.error(f"Error while retrieving village with code {code_village}: {e}")
            raise e
        except Exception as e:
            self.logger.error(f"Error while retrieving village with code {code_village}: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
