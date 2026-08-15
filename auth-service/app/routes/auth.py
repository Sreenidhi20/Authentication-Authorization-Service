from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import SignupRequest, UserResponse
from app.services import auth_service

router = APIRouter(tags=["auth"])


@router.post("/signup", response_model=UserResponse, status_code=201)
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    user = auth_service.signup_user(db, payload)
    return user
