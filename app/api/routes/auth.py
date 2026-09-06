from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.auth import UserRegister, UserLogin, UserOut, Token
from app.services.auth_service import register_user, login_user
from app.api.dependencies import get_current_user
from app.models.user import User
from app.cache.rate_limiter import check_rate_limit

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut, status_code=201)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    return register_user(db, payload)


@router.post("/login", response_model=Token)
async def login(payload: UserLogin, request: Request, db: Session = Depends(get_db)):
    client_ip = request.client.host if request.client else "unknown"
    await check_rate_limit(f"rate_limit:login:{client_ip}", max_requests=5, window_seconds=60)

    token = login_user(db, payload)
    return Token(access_token=token)


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user