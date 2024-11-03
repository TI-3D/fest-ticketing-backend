from app.repositories.auth_repository import AuthRepository
from app.schemas.auth import SignupRequest, SigninRequest, GoogleSigninRequest, SignupResponse, SigninResponse, TokenData
from app.models.user import User
from app.models.auth import EmailAuthentication, GoogleAuthentication
from app.core.security import verify_password, hash_password, create_access_token, verify_google_id_token
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from app.core.config import settings, Logger
from app.repositories.personal_access_token_repository import PersonalAccessTokenRepository
from app.core.exception import (
    NotFoundException,
    ServerErrorException,
    UnauthorizedException,
    BadRequestException
)

class AuthService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.logger = Logger(__name__).get_logger()
        self.auth_repository = AuthRepository(db)
        self.personal_access_token_repository = PersonalAccessTokenRepository(db)

    async def signup(self, request: SignupRequest) -> SignupResponse:
        self.logger.debug(f"Signing up user: {request.email}")
        user_exist = await self.auth_repository.get_user_by_email(request.email)
        if user_exist:
            self.logger.error(f"Signup failed: User already exists with email {request.email}")
            raise BadRequestException("User already exists")
        
        try:
            user = User(
                user_id=ObjectId(),
                full_name=request.full_name,
                email=request.email,
                gender=request.gender
            )
            email_auth = EmailAuthentication(
                email_authentication_id=ObjectId(),
                password=hash_password(request.password),
                user_id=user.user_id
            )
            await self.auth_repository.create_user(user, email_auth)
            self.logger.info(f"User created successfully: {user.email}")
            return SignupResponse(
                message="User created successfully"
            )
        except BadRequestException as e:
            self.logger.exception("BadRequestException during signup")
            raise e
        except Exception:
            self.logger.exception("Unexpected error during signup")
            raise e

    async def signin(self, request: SigninRequest) -> SigninResponse:
        self.logger.debug(f"Signing in user: {request.email}")
        try:
            user = await self.auth_repository.get_user_by_email(request.email)
            if not user:
                self.logger.error(f"Signin failed: User not found with email {request.email}")
                raise NotFoundException("User not found")
            
            email_auth = await self.auth_repository.get_email_authentication_by_user_id(user.user_id)
            if not email_auth or not verify_password(request.password, email_auth.password):
                self.logger.error("Signin failed: Invalid email or password")
                raise BadRequestException("Invalid email or password")
            
            personal_token = await self.personal_access_token_repository.create_token(user.user_id, user.email, request.device_id)
            self.logger.info(f"User signed in successfully: {user.email}")
            return SigninResponse(
                message="User signed in successfully",
                data={"user": user.model_dump()},
                token={
                    "access_token": TokenData(
                        token=personal_token.access_token,
                        token_type="Bearer",
                        expires_in=settings.get_access_token_expires
                    )
                }
            )
        except NotFoundException as e:
            self.logger.exception("NotFoundException during signin")
            raise e
        except BadRequestException as e:
            self.logger.exception("BadRequestException during signin")
            raise e
        except Exception:
            self.logger.exception("Unexpected error during signin")
            raise e

    async def google_signin(self, request: GoogleSigninRequest) -> SigninResponse:
        self.logger.debug("Signing in user with Google")
        payload = verify_google_id_token(request.google_id)
        if not payload:
            self.logger.error("Invalid Google ID token")
            raise ValueError("Invalid Google ID token")
        
        email = payload['email']
        user = await self.auth_repository.get_user_by_email(email)
        if not user:
            self.logger.debug(f"Creating new user from Google sign-in: {email}")
            user = User(
                user_id=ObjectId(),
                full_name=payload.get('name', ''),
                email=email,
                google_id=payload['sub']
            )
            google_auth = GoogleAuthentication(
                google_authentication_id=ObjectId(),
                google_id=payload['sub'],
                user=user
            )
            await self.auth_repository.create_user(user, google_auth)
        
        access_token = create_access_token(user_id=user.user_id, email=user.email, is_google=True)
        self.logger.info(f"User signed in successfully with Google: {user.email}")
        return SigninResponse(
            message="User signed in successfully",
            data={"user": user.model_dump()},
            token={
                "access_token": TokenData(
                    token=access_token,
                    token_type="Bearer",
                    expires_in=settings.get_access_token_expires
                )
            }
        )
    
    async def signout(self, access_token: str):
        try:
            token_entry = await self.personal_access_token_repository.delete_token(access_token)
            if not token_entry:
                self.logger.error("Signout failed: Token not found")
                raise NotFoundException("Token not found")

            self.logger.info(f"User signed out successfully: Token invalidated")
            return {"message": "User signed out successfully"}
        
        except UnauthorizedException as e:
            self.logger.exception("UnauthorizedException during signout")
            raise e
        except NotFoundException as e:
            self.logger.exception("NotFoundException during signout")
            raise e
        except Exception as e:
            self.logger.exception("Unexpected error during signout")
            raise e
