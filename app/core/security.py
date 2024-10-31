from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from uuid import UUID
from app.core.config import settings
from google.oauth2 import id_token
from google.auth.transport import requests
from app.dependencies import redis_client

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

def create_access_token(user_id: UUID, email: str, is_google: bool):
    to_encode = {"sub": str(user_id), "email": email, "is_google": is_google}
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        stored_token = redis_client.get(user_id)
        if stored_token and stored_token.decode('utf-8') == refresh_token:
            return user_id
    except JWTError:
        return None

def verify_google_id_token(id_token_str: str):
    try:
        idinfo = id_token.verify_oauth2_token(id_token_str, requests.Request(), settings.GOOGLE_CLIENT_ID)
        return idinfo
    except ValueError:
        return None