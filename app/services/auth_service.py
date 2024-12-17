from fastapi import HTTPException
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, PersonalAccessToken, Provider, ProviderName, VerificationType, Role
from app.repositories import UserRepository, PersonalAccessTokenRepository,ProviderRepository
from app.services.otp_service import OTPService
from app.schemas.auth import SignupRequest, SigninRequest, SignupResponse, SigninResponse, TokenClaim
from app.schemas.response import ResponseModel, ResponseSuccess
from app.schemas.user import UserBase
from app.core.security import generate_password_hash, check_password_hash, create_jwt_token, verify_jwt_token
from app.core.config import settings
from app.schemas.otp import VerifyOtpRequest, VerifyOtpResponse, SendOtpRequest, SendOtpResponse
from typing import Optional

class AuthService:
    def __init__(self, session: AsyncSession):
        self.user_repository = UserRepository(session)
        self.personal_access_token = PersonalAccessTokenRepository(session)
        self.provider_repository = ProviderRepository(session)
        self.otp_service = OTPService(session)
        self.session = session

    async def signup(self, signup_data: SignupRequest, client_ip: str) -> SignupResponse:
        """
        Sign up a new user or update an existing unverified user and send an OTP for verification.
        """
        async with self.session.begin():  # Manage transaction at the service layer
            # Check if NIK already exists            
            existing_user = await self.user_repository.get_user_by_email(signup_data.email)
            if existing_user:
                provider = await self.provider_repository.get_by_provider_name_by_user_id(existing_user.user_id)
                if existing_user.email_verified_at is None or (provider is not None and provider.provider_name != ProviderName.EMAIL):
                    updated_data = {
                        "full_name": signup_data.full_name,
                        "email": signup_data.email,  # Allow email change
                        "gender": signup_data.gender,
                        "password_hash": generate_password_hash(signup_data.password),
                    }
                    await self.user_repository.update(existing_user.user_id, updated_data)
                    user = existing_user  # Keep reference to updated user
                else:
                    raise HTTPException(status_code=400, detail="Email is already registered and verified.")
            else:
                password_hash = generate_password_hash(signup_data.password)
                user = User(
                    full_name=signup_data.full_name,
                    email=signup_data.email,
                    password_hash=password_hash,
                    gender=signup_data.gender,
                )
                provider = Provider(
                    provider_name=ProviderName.EMAIL,
                    user=user,
                )
                provider = await self.provider_repository.create(provider)
                user = await self.user_repository.create(user)
            # Generate OTP and send it via email
            otp_model = await self.otp_service.generate_and_save(user.user_id, VerificationType.REGISTRATION, client_ip)
            
            return SignupResponse(
                message="Registration successful. Check your email for OTP verification", 
                data={
                    "email": user.email,
                    "hash": otp_model.hashed_otp
                },
            )
            
    async def send_otp(self, send_otp_data: SendOtpRequest, client_ip: str) -> SendOtpResponse:
        """
        Send an OTP to the user's email for verification.
        """
        async with self.session.begin():
            user = await self.user_repository.get_user_by_email(send_otp_data.email)

            if not user:
                raise HTTPException(status_code=400, detail="User not found")

            # Generate OTP and send it via email
            otp_model = await self.otp_service.regenerate_otp(user.user_id, client_ip)         
            
            return SendOtpResponse(
                message="OTP sent successfully",
                data={
                    "email": user.email,
                    "hash": otp_model.hashed_otp
                }
            )
    
    async def verify(self, verify_data: VerifyOtpRequest) -> SigninResponse:
        """
        Verify the OTP sent to the user's email.
        """
        async with self.session.begin():
            user = await self.user_repository.get_user_by_email(verify_data.email)

            if not user:
                raise HTTPException(status_code=400, detail="User not found")

            # Verify the OTP
            otp_type = await self.otp_service.verify_otp(verify_data)

            if not otp_type:
                raise HTTPException(status_code=400, detail="Invalid or expired OTP")
            if otp_type == VerificationType.REGISTRATION:
                token = await self.create_personal_access_token(user.user_id, user.role, verify_data.device_id)
                if not token:
                    raise HTTPException(status_code=400, detail="Invalid credentials")
                return SigninResponse(
                    message="Email verified successfully",
                    data={
                        "user": UserBase.model_validate(user),
                    },
                    token={
                        "access_token": {
                            "token": token.access_token,
                            "token_type": "Bearer",
                            "expires_in": int((token.expires_at - datetime.now(timezone.utc)).total_seconds())
                        }
                    }
                )

            return VerifyOtpResponse(
                message="Email verified successfully",
            )

    async def signin(self, signin_data: SigninRequest,  is_admin = False) -> SigninResponse:
        """
        Sign in an existing user, validate the credentials and check OTP verification.
        """
        
        async with self.session.begin():  # Begin transaction at the service level
            user = await self.user_repository.get_user_by_email(signin_data.email)
            if not user:
                raise HTTPException(status_code=400, detail="Invalid email or password")
            provider = await self.provider_repository.get_by_provider_name_by_user_id(user.user_id)
            if provider is not None and provider.provider_name == ProviderName.EMAIL:
                if not check_password_hash(signin_data.password, user.password_hash):
                    raise HTTPException(status_code=400, detail="Invalid email or password")       
            
            # if user.email_verified_at is None:
            #     raise HTTPException(status_code=400, detail="Email not verified")
            
            if not is_admin and user.role == Role.ADMIN:
                raise HTTPException(status_code=403, detail="Forbidden")
            token = await self.create_personal_access_token(user.user_id, user.role, signin_data.device_id)
            if not token:
                raise HTTPException(status_code=400, detail="Invalid credentials")
            return SigninResponse(
                message="Sign in successful",
                data={
                    "user": UserBase.model_validate(user),    
                },
                token={
                    "access_token": {
                        "token": token.access_token,
                        "token_type": "Bearer",
                        "expires_in": int((token.expires_at - datetime.now(timezone.utc)).total_seconds())
                    }
                }
                
            )
            
    async def create_personal_access_token(self, user_id: str, role: Role, device_id: Optional[str]) -> PersonalAccessToken:
        # Generate JWT token for the user
            payload = {
                "sub": str(user_id),
                "role": str(role),
            }

            jwt_token = create_jwt_token(payload)

            # Generate a personal access token for the user
            token = PersonalAccessToken(
                user_id=user_id,
                device_id=device_id,
                access_token=jwt_token,
                created_at=datetime.now(timezone.utc),
                expires_at=datetime.now(timezone.utc) + timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)
            )
            await self.personal_access_token.create_token(token)
            
            return token
            
    async def get_current_user(self, user_id: str) -> ResponseSuccess:
        """
        Get the current user based on the personal access token.
        """
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return ResponseSuccess(
            message="User found",
            data={
                "user": UserBase.model_validate(user)
            }
        )
        

    async def signout(self, token: str) ->bool:
        """
        Sign out the user by deleting the personal access token.
        """
        async with self.session.begin():
            personal_token = await self.personal_access_token.get_token_by_token(token)
            print(personal_token)
            if not personal_token:
                raise HTTPException(status_code=400, detail="Invalid credentials")
            
            verify_token = verify_jwt_token(personal_token.access_token)
            await self.personal_access_token.delete_token(personal_token.token_id)
            return ResponseSuccess(message="Sign out successful", data={
                "status": "success"
            })
