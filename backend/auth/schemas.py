from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserBase(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None


class UserCreate(UserBase):
    password: str


class User(BaseModel):
    disabled: bool | None = None

    class Config:
        from_attributes = True
