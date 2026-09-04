from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repository import get_user_by_email, create_user
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.auth import UserRegister, UserLogin


def register_user(db: Session, payload: UserRegister):
    existing = get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists.",
        )
    hashed = hash_password(payload.password)
    return create_user(db, payload.name, payload.email, hashed)


def login_user(db: Session, payload: UserLogin) -> str:
    user = get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )
    token = create_access_token(data={"sub": str(user.id)})
    return token