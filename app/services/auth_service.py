import uuid
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        now = datetime.now(timezone.utc)
        
        if expires_delta:
            expire = now + expires_delta
        else:
            expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            
        to_encode.update({
            "exp": expire,
            "iat": now,
            "nbf": now,
            "jti": str(uuid.uuid4()),
            "iss": settings.JWT_ISSUER,
            "aud": settings.JWT_AUDIENCE,
            "type": "access"
        })
        
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
