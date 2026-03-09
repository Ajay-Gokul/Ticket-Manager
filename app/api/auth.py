from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.db.database import get_db
from app.models.schemas import UserLogin, Token, UserCreate
from app.services.user_service import UserService
from app.core.config import settings
from app.core.exceptions import UnauthorizedException
from app.repositories.user_repository import UserRepository
from app.models.db_models import User

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise UnauthorizedException("Could not validate credentials")
    except JWTError:
        raise UnauthorizedException("Could not validate credentials")
    
    user_repo = UserRepository(db)
    user = user_repo.get_user_by_email(email)
    if user is None:
        raise UnauthorizedException("User not found")
    return user

@router.post("/login", response_model=Token)
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.authenticate_user(user_login)

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user_service.register_user(user_in)
    return {"msg": "User created successfully"}

@router.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        "UID": current_user.UID,
        "Name": current_user.Name,
        "Email": current_user.Email,
        "Role": current_user.role.Name # Assuming relationship is set
    }
