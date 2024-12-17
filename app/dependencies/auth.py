from app.core.exception import (UnauthorizedException, ServerErrorException)
from fastapi.requests import Request
from app.core.security import verify_jwt_token
from typing import Dict
from fastapi import Depends
from app.repositories import PersonalAccessTokenRepository

async def get_access_token(request: Request) -> str:
    try:
        authorization = request.headers.get("Authorization")
        if not authorization:
            raise UnauthorizedException("Invalid Credentials")
        token = authorization.split()[1]
        return token
    except UnauthorizedException as e:
        raise UnauthorizedException(str(e)) from e
    except Exception as e:
        raise ServerErrorException("An error occurred while getting the access token")
    
async def get_current_user(request: Request) -> Dict:
    try:
        
        token = await get_access_token(request)
        return await get_user_by_token(token)        
    except UnauthorizedException as e:
        raise UnauthorizedException(str(e)) from e
    except Exception as e:
        raise ServerErrorException("An error occurred while getting the user") from e
    
async def get_user_by_token(token: str) -> Dict:
    try:
        payload = verify_jwt_token(token)
        return payload
    except UnauthorizedException as e:
        raise UnauthorizedException(str(e)) from e
    except Exception as e:
        raise ServerErrorException("An error occurred while getting the user") from e
    

async def get_optional_user(request: Request) -> Dict:
    try:
        token = await get_access_token(request)
        payload = verify_jwt_token(token)
        return payload
    except UnauthorizedException as e:
        return None
    except Exception as e:
        raise ServerErrorException("An error occurred while getting the user") from e
    
