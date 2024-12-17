from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt, ExpiredSignatureError
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from app.core.config import settings, logger
from app.schemas.auth import TokenClaim
import pyotp

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
def create_jwt_token(data: TokenClaim | dict[str, str], expires_in: timedelta = None) -> str:
    """
    Membuat token JWT dengan data payload dan waktu kadaluarsa opsional.
    """
    # Mengonversi data ke dict
    # to_encode = data.model_dump()
    
    if isinstance(data, TokenClaim):
        to_encode = data.model_dump()
    else:
        to_encode = data
    
    if expires_in:
        expire = datetime.now(timezone.utc) + expires_in  # Gunakan waktu UTC
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)  # Default kadaluarsa 1 hari
    
    # Mengonversi waktu expire menjadi\\\ Unix timestamp
    expire_timestamp = expire.timestamp()
    
    # Menambahkan exp ke payload
    to_encode.update({"exp": expire_timestamp})
    
    try:
        # Menggunakan JWT dengan secret key dan algoritma yang sesuai
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error encoding JWT: {e}")
        raise HTTPException(status_code=500, detail="Error generating JWT token")

# Function untuk memverifikasi token JWT
def verify_jwt_token(token: str) -> dict:
    """
    Memverifikasi token JWT dan mengembalikan payload data jika valid.
    """
    try:        # Decode token dan pastikan expired signature error ditangani dengan benar
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], options={"require_exp": True})
        
        # Verifikasi apakah token kadaluarsa
        if payload['exp'] < datetime.now(timezone.utc).timestamp():
            raise ExpiredSignatureError
        
        return payload
    except ExpiredSignatureError:
        logger.error("Token has expired")
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError as e:
        logger.error(f"Error verifying JWT token: {e}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        logger.error(f"Unexpected error verifying JWT token: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
def generate_otp_secret() -> str:
    """Generate a random OTP secret."""
    totp = pyotp.random_base32()
    return totp

def verify_otp(otp_code: str, secret: str, created_at: datetime, expires_in: int) -> bool:
    """Verify OTP for specific verification type"""

    # Jika `created_at` tidak memiliki zona waktu, beri zona waktu UTC
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)
    
    expires_at = created_at + timedelta(seconds=expires_in)
    
    # Membandingkan datetime offset-aware
    if datetime.now(timezone.utc) > expires_at:
        raise HTTPException(status_code=400, detail="OTP expired")
    
    totp = pyotp.TOTP(secret)
    is_valid = totp.verify(otp_code)
    print("is_valid", is_valid)
    
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    return True