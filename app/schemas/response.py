from pydantic import BaseModel
from datetime import datetime
from typing import Any, Optional, List

class ErrorDetail(BaseModel):
    field: str
    message: str

class ResponseModel(BaseModel):
    code: int
    timestamp: datetime
    message: str
    
    class Config:
        from_attributes = True
        exlude_none = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ResponseSuccess(ResponseModel):
    data: Optional[Any] = None
    
    class Config:
        from_attributes = True
        exlude_none = True
    
class ResponseError(ResponseModel):
    errors: List[ErrorDetail]
