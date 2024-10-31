from app.core.config import settings
import redis
import motor.motor_asyncio
from motor.core import AgnosticDatabase

# Create the MongoDB client and select the database
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)
mongo_db: AgnosticDatabase = mongo_client[settings.MONGO_DB_NAME]

# Initialize Redis client
redis_client = redis.StrictRedis(
    username=settings.REDIS_USERNAME,
    password=settings.REDIS_PASSWORD,
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True  # Optional, to decode responses as strings
)

# MongoDB getter function for FastAPI dependency injection
def get_mongo_db():
    if mongo_db is not None:  # Assuming mongo_db is your initialized AsyncIOMotorDatabase instance
        return mongo_db
    else:
        raise RuntimeError("Failed to initialize MongoDB client.")

# Redis getter function for FastAPI dependency injection
def get_redis():
    return redis_client
