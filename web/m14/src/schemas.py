from datetime import datetime, date

from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    date_of_birth: date


class ContactResponse(BaseModel):
    id: int = Field(ge=1)
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    date_of_birth = date
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str = None

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr