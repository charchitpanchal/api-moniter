from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.auth import UserRegister, UserLogin, UserOut, Token
from app.services.auth_service import register_user, login_user
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut, status_code=201)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    return register_user(db, payload)


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    token = login_user(db, payload)
    return Token(access_token=token)


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user