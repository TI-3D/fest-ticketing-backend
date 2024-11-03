from app.core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticDatabase
from beanie import init_beanie
from app.models.user import User
from app.models.auth import Authentication, EmailAuthentication, GoogleAuthentication
from app.models.personal_access_token import PersonalAccessToken

# Create the MongoDB client and select the database
mongo_client = AsyncIOMotorClient(settings.MONGO_URI)
mongo_db: AgnosticDatabase = mongo_client[settings.MONGO_DB_NAME]

async def init_db():
    """Initializes the Beanie ODM with the provided document models."""
    await init_beanie(
        database=mongo_db,  # Use the already initialized mongo_db
        document_models=[
            User,
            Authentication,
            EmailAuthentication,
            GoogleAuthentication,
            PersonalAccessToken
        ]
    )

# MongoDB getter function for FastAPI dependency injection
def get_mongo_db() -> AgnosticDatabase:
    """Returns the initialized MongoDB database."""
    if mongo_db is not None:  # Ensure the database instance is initialized
        return mongo_db
    else:
        raise RuntimeError("Failed to initialize MongoDB client.")
