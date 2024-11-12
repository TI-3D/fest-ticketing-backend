from fastapi import HTTPException
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from app.core.config import settings, logger
# Set up password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function untuk memverifikasi password plain dan hashed
def check_password_hash(plain_password: str, hashed_password: str) -> bool:
    """
    Memverifikasi apakah password plain cocok dengan hashed password menggunakan argon2.
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError:
        logger.error("Unknown hash error occurred while verifying password")
        return False
    except Exception as e:
        logger.error(f"Error verifying password: {e}")
        return False

# Function untuk meng-hash password
def generate_password_hash(password: str) -> str:
    """
    Meng-hash password plain menggunakan argon2.
    """
    return pwd_context.hash(password)


        
# Function untuk meng-generate token JWT
def create_jwt_token(data: dict, expires_at: datetime = None) -> str:
    """
    Membuat token JWT dengan data payload dan waktu kadaluarsa opsional.
    """
    to_encode = data.copy()
    if expires_at:
        expire = expires_at
    else:
        expire = datetime.now() + timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# Function untuk memverifikasi token JWT
def verify_jwt_token(token: str) -> dict:
    """
    Memverifikasi token JWT dan mengembalikan payload data jika valid.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError as e:
        logger.error(f"Error verifying JWT token: {e}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        logger.error(f"Unexpected error verifying JWT token: {e}")
        raise
