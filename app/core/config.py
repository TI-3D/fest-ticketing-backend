from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    APP_NAME: str = "Fest Ticketing"
    APP_ENV: str = "development"
    
    MONGO_USERNAME: str
    MONGO_PASSWORD: str
    MONGO_SERVER: str = "localhost"
    MONGO_PORT: int = 27017
    MONGO_DB_NAME: str  = "fest_ticketing"

    @property
    def MONGO_URI(self) -> str:
        if self.MONGO_USERNAME and self.MONGO_PASSWORD:
            return f"mongodb+srv://{self.MONGO_USERNAME}:{self.MONGO_PASSWORD}@{self.MONGO_SERVER}:{self.MONGO_PORT}"
        return f"mongodb://{self.MONGO_SERVER}:{self.MONGO_PORT}"
    
    
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_USERNAME: str | None = 'root'
    REDIS_PASSWORD: str | None = None
    REDIS_DB: int = 0
    
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 587
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAILS_FROM_EMAIL: str | None = None
    EMAILS_FROM_NAME: str | None = None

    EMAIL_RESET_TOKEN_EXPIRE_MINUTES: int = 5
    
    class Config:
        env_file = ".env"

settings = Settings()
