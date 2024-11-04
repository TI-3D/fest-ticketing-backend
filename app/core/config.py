from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Fest Ticketing"
    APP_ENV: str = "development"
    APP_HOST: str = "localhost"
    APP_PORT: int = 8000
    
    API_V1: str = "/api/v1/"
    
    MONGO_SRV: bool = False
    MONGO_USERNAME: str
    MONGO_PASSWORD: str
    MONGO_SERVER: str = "localhost"
    MONGO_PORT: int = 27017
    MONGO_DB_NAME: str  = "fest_ticketing"

    @property
    def MONGO_URI(self) -> str:
        connection = "mongodb+srv" if self.MONGO_SRV else "mongodb"
        if self.MONGO_USERNAME and self.MONGO_PASSWORD:
            return f"{connection}://{self.MONGO_USERNAME}:{self.MONGO_PASSWORD}@{self.MONGO_SERVER}:{self.MONGO_PORT}"
        else:
            return f"{connection}://{self.MONGO_SERVER}:{self.MONGO_PORT}"
    
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 30
    @property
    def get_access_token_expires(self) -> int:
        return (self.ACCESS_TOKEN_EXPIRE_DAYS * 24 * 60 * 60)
    
    # CORS_ORIGINS: list[str] | str = []
    
    # GOOGLE_CLIENT_ID: str
    
    SECURE_COOKIE: bool = False
    
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 587
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAILS_FROM_EMAIL: str | None = None
    EMAILS_FROM_NAME: str | None = None

    EMAIL_RESET_TOKEN_EXPIRE_MINUTES: int = 5
    
    AUTH_EXCLUDED_PATHS: list[str] = [
        "/",
        "/api/v1/auth/signup", 
        "/api/v1/auth/signin", 
        "/api/v1/auth/google-signin", 
        ]
    
    class Config:
        env_file = ".env"

settings = Settings()

import logging

class Logger:
    def __init__(self, name: str):
        self.logger = self.setup_logging(name)

    def setup_logging(self, name: str) -> logging.Logger:
        # Create a custom logger
        logger = logging.getLogger(name)

        # Set the default log level
        logger.setLevel(logging.DEBUG)

        # Create handlers
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler('app.log')

        # Set level for handlers
        console_handler.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.INFO)

        # Create formatters and add them to handlers
        console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]')

        console_handler.setFormatter(console_format)
        file_handler.setFormatter(file_format)

        # Add handlers to the logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger

    def get_logger(self) -> logging.Logger:
        return self.logger


# Usage
logger = Logger(__name__).get_logger()