from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Fest Ticketing"
    APP_ENV: str = "development"
    APP_HOST: str = "localhost"
    APP_PORT: int = 8000
    
    API_V1: str = "/api/v1/"
    
    DB_CONNECTION: str = "mysql" # mysql, postgresql, sqlite, sqlserver, etc
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str  = "fest_ticketing"
    
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """
        Menghasilkan URL koneksi yang sesuai berdasarkan konfigurasi database.
        """
        if self.DB_CONNECTION == "sqlite":
            # SQLite tidak memerlukan username dan password, cukup dengan file database
            return f"sqlite:///{self.DB_NAME}.db"  # Biasanya file path untuk SQLite
        elif self.DB_CONNECTION == "mysql":
            if self.DB_USER and self.DB_PASSWORD:
                return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            else:
                return f"mysql+pymysql://{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        elif self.DB_CONNECTION == "postgresql":
            if self.DB_USER and self.DB_PASSWORD:
                return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            else:
                return f"postgresql+psycopg://{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        elif self.DB_CONNECTION == "mssql":
            if self.DB_USER and self.DB_PASSWORD:
                return f"mssql+pyodbc://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?driver=SQL+Server"
            else:
                return f"mssql+pyodbc://{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?driver=SQL+Server"
        else:
            raise ValueError(f"Unsupported DB_CONNECTION: {self.DB_CONNECTION}")
    
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 30
    @property
    def get_access_token_expires(self) -> int:
        return (self.ACCESS_TOKEN_EXPIRE_DAYS * 24 * 60 * 60)
    
    # CORS_ORIGINS: list[str] | str = []
    
    # GOOGLE_CLIENT_ID: str
    
    
    SMTP_PORT: int = 587
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAILS_FROM_EMAIL: str | None = None
    EMAILS_FROM_NAME: str | None = None

    EMAIL_RESET_TOKEN_EXPIRE_MINUTES: int = 5
    
    AUTH_EXCLUDED_PATHS: list[str] = [
        "/",
        "/docs",
        "/openapi.json",
        "/api/v1/auth/signup", 
        "/api/v1/auth/signin",  
        "/api/v1/auth/google-signin", 
        "/api/v1/auth/send-otp",
        "/api/v1/auth/verification",
        
        
        "/api/v1/location/provinces",
        
        "/api/v1/organizer",
        
        "/api/v1/event",
        "/api/v1/event/categories",
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