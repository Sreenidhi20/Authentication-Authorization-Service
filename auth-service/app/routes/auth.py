from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import SignupRequest, UserResponse
from app.schemas.token import LoginRequest, TokenResponse
from app.services import auth_service

router = APIRouter(tags=["auth"])


@router.post("/signup", response_model=UserResponse, status_code=201)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    user = auth_service.signup_user(db, payload)
    return user

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    access_token = auth_service.login_user(db, payload)
    return TokenResponse(access_token=access_token, token_type="bearer")