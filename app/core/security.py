from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from bson import ObjectId
from app.core.config import settings, logger
from google.oauth2.id_token import verify_token
from google.oauth2 import id_token
from google.auth.transport import requests
from app.schemas.auth import TokenData
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.exception import (UnauthorizedException)

# Set up password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to verify plain and hashed passwords
def verify_password(plain_password, hashed_password) -> bool:
    try:
        result = pwd_context.verify(plain_password, hashed_password)
        if not result:
            logger.warning("Password verification failed for user.")
        return result
    except ValueError as e:
        logger.error(f"Error verifying password: {e}")
        raise UnauthorizedException("Invalid credentials")

# Function to hash password
def hash_password(password) -> str:
    try:
        hashed = pwd_context.hash(password)
        logger.info("Password hashed successfully.")
        return hashed
    except Exception as e:
        logger.error(f"Error hashing password: {e}")
        return None

def create_access_token(user_id: ObjectId, email: str, is_google: bool) -> TokenData:
    to_encode = {"sub": str(user_id), "email": email, "is_google": is_google}
    expire = datetime.now() + timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    logger.info(f"Access token created for user {user_id}.")
    return TokenData(token=encoded_jwt, token_type="Bearer", expires_in=settings.ACCESS_TOKEN_EXPIRE_DAYS * 24 * 60 * 60)

async def verify_access_token(db: AsyncIOMotorDatabase, access_token: str) -> ObjectId:
    try:
        token = await db["personal_access_tokens"].find_one({"access_token": access_token})
        if not token:
            logger.warning(f"Personal access token not found for access token: {access_token}.")
            raise UnauthorizedException("Invalid credentials")
        if not token or token['access_token_expired'] < datetime.now():
            logger.warning(f"Personal access token not found for access token: {access_token}.")
            raise UnauthorizedException("Invalid credentials")
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if not user_id or user_id != str(token['user_id']):
            logger.warning("No user ID found in access token.")
            raise UnauthorizedException("Invalid credentials")
        logger.info(f"Access token verified for user {user_id}")
        return ObjectId(user_id)
    except UnauthorizedException as e:
        logger.warning(f"Unauthorized access attempt with token: {access_token}")
        raise e
    except JWTError as e:
        logger.error(f"JWT error during access token verification: {e}")
        raise UnauthorizedException("Token verification failed")

def verify_google_id_token(google_id: str) -> dict:
    try:
        user_info = id_token.verify_oauth2_token(google_id, requests.Request(), settings.GOOGLE_CLIENT_ID)
        logger.info("Google ID token verified successfully.")
        return user_info
    except ValueError as e:
        logger.error(f"Invalid Google ID token: {e}")
        raise UnauthorizedException("Invalid Google ID token")
