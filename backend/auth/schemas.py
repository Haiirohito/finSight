from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserBase(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None


class UserCreate(UserBase):
    password: str


class ForgotPassword(BaseModel):
    email: str


class ResetPassword(BaseModel):
    token: str
    new_password: str


class User(UserBase):
    disabled: bool | None = None

    class Config:
        from_attributes = True
