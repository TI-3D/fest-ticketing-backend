from fastapi import HTTPException, status


class RedirectionException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_302_FOUND, detail=message)

class BadRequestException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

class UnauthorizedException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)

class ForbiddenException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=message)

class NotFoundException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)

class ServerErrorException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message)
