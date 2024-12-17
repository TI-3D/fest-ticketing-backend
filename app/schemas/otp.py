from app.schemas.response import ResponseModel
from pydantic import  EmailStr, BaseModel
from datetime import datetime
from typing import Optional

class SendOtpRequest(BaseModel):
    email: EmailStr

class VerifyOtpRequest(BaseModel):
    hash: str
    email: EmailStr
    otp: str
    device_id: Optional[str] = None
    
class VerifyOtpResponse(ResponseModel):
    pass

class SendOtpResponse(ResponseModel):
    data: Optional[dict] = None
    

