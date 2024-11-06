from beanie import Document, Link, PydanticObjectId
from datetime import datetime
from pydantic import Field, EmailStr

class OTP(Document):
    otp_id: PydanticObjectId = Field(default_factory=PydanticObjectId, primary_key=True)
    email: EmailStr = Field(description="Email address to send OTP")
    hash: str = Field(description="Hashed OTP")
    otp: str = Field(description="OTP code")
    expiration: datetime  = Field(description="Expiration time of OTP")
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Settings:
        collection = "otps"
