from app.core.exception import (UnauthorizedException, ServerErrorException)
from fastapi.requests import Request
from app.core.config import settings

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
    
