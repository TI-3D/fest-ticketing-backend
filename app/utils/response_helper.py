from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Any, Dict

class ResponseHelper:
    def __init__(self):
        self.status_code = 200
        self.content = {}

    def status(self, status_code: int) -> 'ResponseHelper':
        self.status_code = status_code
        return self

    def json(self, content: Dict[str, Any]) -> JSONResponse:
        self.content = self.serialize_content(content)
        self.content["code"] = self.status_code
        return JSONResponse(content=self.content, status_code=self.status_code)

    @staticmethod
    def serialize_content(content: Dict[str, Any]) -> Dict[str, Any]:
        serialized_content = {}
        for key, value in content.items():
            if isinstance(value, datetime):
                serialized_content[key] = value.isoformat()
            elif value is not None:
                serialized_content[key] = value
        return serialized_content

ResponseHelper = ResponseHelper()