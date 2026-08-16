from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import SignupRequest
from app.schemas.token import LoginRequest
from app.core.security import hash_password, verify_password, create_access_token



def signup_user(db: Session, payload: SignupRequest) -> User:
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )

    user = User(
        name=payload.name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role="user",
        is_verified=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, payload: LoginRequest) -> str:
    """Verifies credentials and returns a signed access token."""
    user = db.query(User).filter(User.email == payload.email).first()

    # Deliberately vague error message — don't reveal whether the email
    # exists or the password was wrong, that distinction helps attackers.
    invalid_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
    )

    if not user:
        raise invalid_credentials

    if not verify_password(payload.password, user.hashed_password):
        raise invalid_credentials

    return create_access_token(user_id=user.id)