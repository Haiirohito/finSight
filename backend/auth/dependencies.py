from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

import jwt
from jwt.exceptions import PyJWTError

from sqlalchemy.orm import Session

from db.dependencies import get_db
from .schemas import TokenData
from .services import get_user

from core.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)

    except PyJWTError:
        raise credentials_exception

    user = get_user(db, username=token_data.username)

    if user is None:
        raise credentials_exception

    return user
