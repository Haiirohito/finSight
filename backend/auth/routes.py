import jwt
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db.dependencies import get_db
from core.config import settings

from .security import create_access_token, get_password_hash, create_refresh_token
from .schemas import Token, UserCreate, User, ForgotPassword, ResetPassword
from .services import authenticate_user, create_user, get_user_by_email
from .dependencies import get_current_user
from .reset_tokens import create_reset_token, verify_reset_token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):

    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    refresh_token = create_refresh_token(data={"sub": user.username})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = get_user_by_email(db, user.email)

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return create_user(db, user)


@router.post("/forgot-password")
def forgot_password(data: ForgotPassword, db: Session = Depends(get_db)):

    user = get_user_by_email(db, data.email)

    if not user:
        return {"message": "If the email exists, a reset link was sent"}

    token = create_reset_token(user.email)

    reset_link = f"http://localhost:3000/reset-password?token={token}"

    # Normally send email here
    print("Reset link:", reset_link)

    return {"message": "Password reset link sent"}


@router.post("/reset-password")
def reset_password(data: ResetPassword, db: Session = Depends(get_db)):

    email = verify_reset_token(data.token)

    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = get_user_by_email(db, email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = get_password_hash(data.new_password)

    db.commit()

    return {"message": "Password updated successfully"}


@router.get("/me", response_model=User)
def read_current_user(current_user=Depends(get_current_user)):
    return current_user


@router.post("/refresh")
def refresh_token(refresh_token: str):

    try:
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token")

        username = payload.get("sub")

        access_token = create_access_token(
            data={"sub": username},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        return {"access_token": access_token}

    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


@router.post("/logout")
def logout():
    return {"message": "User logged out"}
