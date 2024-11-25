from fastapi import APIRouter, Depends, Response, Request, HTTPException
from fastapi.responses import JSONResponse
from app.dependencies import get_access_token, get_db
from app.core.config import Logger
from app.schemas.response import ResponseModel, ResponseSuccess
from app.services.location_service import LocationService
from datetime import datetime
router = APIRouter()
logger = Logger(__name__).get_logger()

@router.get("/provinces", response_model=ResponseModel)
async def get_provinces(
    db=Depends(get_db)
):
    """
    Retrieve all provinces.
    """
    location_service = LocationService(db)
    try:
        provinces = await location_service.get_provinces()
        return JSONResponse(content=ResponseSuccess(
            timestamp=datetime.now(),   
            message="Provinces retrieved successfully",
            data=provinces).model_dump(), status_code=200)
    except HTTPException as e:
        logger.error(f"Error while retrieving provinces: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error while retrieving provinces: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/provinces/{code_province}", response_model=ResponseModel)
async def get_province_by_code(
    code_province: str,
    db=Depends(get_db)
):
    """
    Retrieve a province by its code.
    """
    location_service = LocationService(db)
    try:
        province = await location_service.get_province_by_code(code_province)
        return JSONResponse(content=ResponseSuccess(
            timestamp=datetime.now(),   
            message="Province retrieved successfully",
            data=province).model_dump(), status_code=200)
    except HTTPException as e:
        logger.error(f"Error while retrieving province with code {code_province}: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error while retrieving province with code {code_province}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/provinces/{code_province}/cities", response_model=ResponseModel)
async def get_cities_by_province(
    code_province: str,
    db=Depends(get_db)
):
    """
    Retrieve all cities in a province.
    """
    location_service = LocationService(db)
    try:
        cities = await location_service.get_cities_by_province(code_province)
        return JSONResponse(content=ResponseSuccess(
            timestamp=datetime.now(),   
            message="Cities retrieved successfully",
            data=cities).model_dump(), status_code=200)
    except HTTPException as e:
        logger.error(f"Error while retrieving cities for province {code_province}: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error while retrieving cities for province {code_province}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/cities/{code_city}", response_model=ResponseModel)
async def get_city_by_code(
    code_city: str,
    db=Depends(get_db)
):
    """
    Retrieve a city by its code.
    """
    location_service = LocationService(db)
    try:
        city = await location_service.get_city_by_code(code_city)
        return JSONResponse(content=ResponseSuccess(
            timestamp=datetime.now(),   
            message="City retrieved successfully",
            data=city).model_dump(), status_code=200)
    except HTTPException as e:
        logger.error(f"Error while retrieving city with code {code_city}: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error while retrieving city with code {code_city}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/cities/{code_city}/districts", response_model=ResponseModel)
async def get_districts_by_city(
    code_city: str,
    db=Depends(get_db)
):
    """
    Retrieve all districts in a city.
    """
    location_service = LocationService(db)
    try:
        districts = await location_service.get_districts_by_city(code_city)
        return JSONResponse(content=ResponseSuccess(
            timestamp=datetime.now(),   
            message="Districts retrieved successfully",
            data=districts).model_dump(), status_code=200)
    except HTTPException as e:
        logger.error(f"Error while retrieving districts for city {code_city}: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error while retrieving districts for city {code_city}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/districts/{code_district}", response_model=ResponseModel)
async def get_district_by_code(
    code_district: str,
    db=Depends(get_db)
):
    """
    Retrieve a district by its code.
    """
    location_service = LocationService(db)
    try:
        district = await location_service.get_district_by_code(code_district)
        return JSONResponse(content=ResponseSuccess(
            timestamp=datetime.now(),   
            message="District retrieved successfully",
            data=district).model_dump(), status_code=200)
    except HTTPException as e:
        logger.error(f"Error while retrieving district with code {code_district}: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error while retrieving district with code {code_district}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/districts/{code_district}/villages", response_model=ResponseModel)
async def get_villages_by_district(
    code_district: str,
    db=Depends(get_db)
):
    """
    Retrieve all villages in a district.
    """
    location_service = LocationService(db)
    try:
        villages = await location_service.get_villages_by_district(code_district)
        return JSONResponse(content=ResponseSuccess(
            timestamp=datetime.now(),   
            message="Villages retrieved successfully",
            data=villages).model_dump(), status_code=200)
    except HTTPException as e:
        logger.error(f"Error while retrieving villages for district {code_district}: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error while retrieving villages for district {code_district}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/villages/{code_village}", response_model=ResponseModel)
async def get_village_by_code(
    code_village: str,
    db=Depends(get_db)
):
    """
    Retrieve a village by its code.
    """
    location_service = LocationService(db)
    try:
        village = await location_service.get_village_by_code(code_village)
        return JSONResponse(content=ResponseSuccess(
            timestamp=datetime.now(),   
            message="Village retrieved successfully",
            data=village).model_dump(), status_code=200)
    except HTTPException as e:
        logger.error(f"Error while retrieving village with code {code_village}: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error while retrieving village with code {code_village}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
