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
    

class SendOtpResponse(BaseModel):
    message: str
    data: Optional[dict] = None
    # field for unicorn response help front end path to post verify otp
    

