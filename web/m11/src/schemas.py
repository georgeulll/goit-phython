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