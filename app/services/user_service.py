from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.repositories.user_repository import UserRepository
from app.repositories.role_repository import RoleRepository
from app.services.auth_service import AuthService
from app.models.schemas import UserCreate, UserLogin, Token
from app.models.db_models import User
from app.core.exceptions import ConflictException, UnauthorizedException, ServerErrorException
from app.core.config import settings

class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        self.role_repo = RoleRepository(db)

    def register_user(self, user_in: UserCreate):               
        if self.user_repo.get_user_by_email(user_in.Email):
            raise ConflictException("Email already registered")
        
        # Security: Automatically assign 'User' role to everyone registering via API
        user_role = self.role_repo.get_role_by_name("User")
        if not user_role:
            raise ServerErrorException("Default User role not found in database")
            
        return self.user_repo.create_user(user_in, user_role.UID)

    def authenticate_user(self, user_login: UserLogin) -> Token:
        user = self.user_repo.get_user_by_email(user_login.Email)
        
        if not user or not AuthService.verify_password(user_login.Password, user.PasswordHash):
            raise UnauthorizedException("Incorrect email or password")
        
h        # Security: Use User UID as subject instead of Email
        access_token = AuthService.create_access_token(data={"sub": str(user.UID)})
        return Token(access_token=access_token, token_type="bearer")

    def get_user_by_email(self, email: str):
        return self.user_repo.get_user_by_email(email)

    def get_current_user(self, token: str) -> User:
        try:
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=[settings.ALGORITHM],
                issuer=settings.JWT_ISSUER,
                audience=settings.JWT_AUDIENCE
            )
            user_id: str = payload.get("sub")
            if user_id is None or payload.get("type") != "access":
                raise UnauthorizedException("Could not validate credentials")
        except JWTError:
            raise UnauthorizedException("Could not validate credentials")
        
        user = self.user_repo.get_user_by_uid(user_id)
        if user is None:
            raise UnauthorizedException("User not found")
        return user
