from pydantic import BaseModel
from datetime import datetime
from typing import Any, Optional, List

class ErrorDetail(BaseModel):
    field: str
    message: str

class ResponseModel(BaseModel):
    code: int = 200
    message: str
    
    class Config:
        from_attributes = True
        exlude_none = True

class ResponseSuccess(ResponseModel):
    data: Optional[Any] = None
    
    class Config:
        from_attributes = True
        exlude_none = True
    
class ResponseError(ResponseModel):
    errors: Optional[List[ErrorDetail]] = None
    
    class Config:
        from_attributes = True
        exlude_none = True
