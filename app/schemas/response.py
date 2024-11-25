from pydantic import BaseModel
from datetime import datetime, timezone
from typing import Any, Optional, List, Dict
from enum import Enum
from uuid import UUID

class ErrorDetail(BaseModel):
    field: str
    message: str

class ResponseModel(BaseModel):
    message: str
    timestamp: Optional[datetime] = datetime.now(timezone.utc)
    
    
    def model_dump(self, *args, **kwargs):
        model_dict = super().model_dump(*args, **kwargs)
        if isinstance(model_dict.get("timestamp"), datetime):
            model_dict["timestamp"] = model_dict["timestamp"].isoformat()
        return model_dict
    
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
