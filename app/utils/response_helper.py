from fastapi.responses import JSONResponse
from fastapi import Response  # Import Response to set cookies
from datetime import datetime
from typing import Any, Dict
from beanie import PydanticObjectId
from app.core.config import settings
from typing import List

class Cookie:
    def __init__(self, name: str, value: str, domain: str = None, path: str = None, expires: int = None, max_age: int = None, secure: bool = False, httponly: bool = False, samesite: str = None):
        self.name = name
        self.value = value
        self.domain = domain
        self.path = path
        self.expires = expires
        self.max_age = max_age
        self.secure = secure
        self.httponly = httponly
        self.samesite = samesite

    def serialize(self) -> str:
        cookie = f"{self.name}={self.value}"
        if self.domain:
            cookie += f"; Domain={self.domain}"
        if self.path:
            cookie += f"; Path={self.path}"
        if self.expires:
            cookie += f"; Expires={self.expires}"
        if self.max_age:
            cookie += f"; Max-Age={self.max_age}"
        if self.secure:
            cookie += "; Secure"
        if self.httponly:
            cookie += "; HttpOnly"
        if self.samesite:
            cookie += f"; SameSite={self.samesite}"
        return cookie

    def set_cookie(self, response: Response):
        response.set_cookie(
            key=self.name,
            value=self.value,
            domain=self.domain,
            path=self.path,
            expires=self.expires,
            max_age=self.max_age,
            secure=self.secure,
            httponly=self.httponly,
            samesite=self.samesite
        )

class ResponseHelper:
    def __init__(self):
        self.status_code = 200
        self.content = {}

    def status(self, status_code: int = 200) -> 'ResponseHelper':
        self.status_code = status_code
        return self

    def json(self, content: Dict[str, Any], response: Response = None, cookies: List[Cookie] = []) -> JSONResponse:
        self.content = self.serialize_content(content)
        self.content["code"] = self.status_code
        
        # Create the JSON response
        json_response = JSONResponse(content=self.content, status_code=self.status_code)
        
        # Set cookies
        for cookie in cookies:
            json_response.set_cookie(
                key=cookie.name,
                value=cookie.value,
                domain=cookie.domain,
                path=cookie.path,
                expires=cookie.expires,
                max_age=cookie.max_age,
                secure=cookie.secure,
                httponly=cookie.httponly,
                samesite=cookie.samesite
            )

        return json_response

    @staticmethod
    def serialize_content(content: Dict[str, Any]) -> Dict[str, Any]:
        serialized_content = {}
        for key, value in content.items():
            if isinstance(value, datetime):
                serialized_content[key] = value.isoformat()
            elif isinstance(value, PydanticObjectId):
                serialized_content[key] = str(value)
            elif isinstance(value, list):
                serialized_content[key] = [ResponseHelper.serialize_content(item) if isinstance(item, dict) else item for item in value]
            elif isinstance(value, dict):
                serialized_content[key] = ResponseHelper.serialize_content(value)
            elif value is not None:
                serialized_content[key] = value
        return serialized_content

ResponseHelper = ResponseHelper()
