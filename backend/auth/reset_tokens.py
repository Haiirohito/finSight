import jwt
from datetime import datetime, timedelta

from core.config import settings


def create_reset_token(email: str):

    expire = datetime.now() + timedelta(minutes=settings.RESET_TOKEN_EXPIRE_MINUTES)

    payload = {"sub": email, "exp": expire, "scope": "password_reset"}

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_reset_token(token: str):

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        if payload.get("scope") != "password_reset":
            return None

        return payload.get("sub")

    except jwt.PyJWTError:
        return None
