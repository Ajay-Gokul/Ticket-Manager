from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.schemas import UserLogin, Token, UserCreate
from app.services.user_service import UserService

router = APIRouter()

@router.post("/login", response_model=Token)
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.authenticate_user(user_login)

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user_service.register_user(user_in)
    return {"msg": "User created successfully"}
