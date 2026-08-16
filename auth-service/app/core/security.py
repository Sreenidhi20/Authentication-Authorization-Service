import bcrypt
import jwt
from datetime import datetime, timedelta, timezone

from app.config import JWT_SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def hash_password(password: str) -> str:
    # bcrypt truncates at 72 bytes silently, so we enforce the limit explicitly
    # rather than let it happen unnoticed.
    password_bytes = password.encode("utf-8")[:72]
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode("utf-8")[:72]
    return bcrypt.checkpw(password_bytes, hashed_password.encode("utf-8"))


def create_access_token(user_id: int, expires_delta: timedelta | None = None) -> str:
    """Generates a signed JWT access token for a user."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),  # subject — the user ID
        "exp": expire,         # expiration time, checked automatically on decode
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Decodes and validates a JWT. Raises jwt exceptions on failure (expired, bad signature, etc)."""
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
