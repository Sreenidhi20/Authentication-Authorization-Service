import bcrypt


def hash_password(password: str) -> str:
    # bcrypt truncates at 72 bytes silently, so we enforce the limit explicitly
    # rather than let it happen unnoticed.
    password_bytes = password.encode("utf-8")[:72]
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode("utf-8")[:72]
    return bcrypt.checkpw(password_bytes, hashed_password.encode("utf-8"))
