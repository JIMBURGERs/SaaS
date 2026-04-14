from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import date, datetime


class UserCreate(BaseModel):
    Email: EmailStr

    Password: str | None = None
    UserName: str
    FirstName: str
    LastName: str
    BirthDate: date | None = None
    Phone: str | None = None

    IsActive: bool = True
    isDeleted: bool = False
    AccountSetup: bool = False


class UserUpdate(BaseModel):
    Email: EmailStr | None = None

    Password: str | None = None
    UserName: str | None = None
    FirstName: str | None = None
    LastName: str | None = None
    BirthDate: date | None = None
    Phone: str | None = None

    LastLogin: datetime | None = None
    IsActive: bool | None = None
    isDeleted: bool | None = None
    AccountSetup: bool | None = None


class UserResponse(BaseModel):
    UserID: int

    Email: EmailStr
    Password: str | None = None
    UserName: str
    FirstName: str
    LastName: str
    BirthDate: date | None = None
    Phone: str | None = None
    
    CreatedAt: datetime
    LastLogin: datetime | None = None
    IsActive: bool
    isDeleted: bool
    AccountSetup: bool

    model_config = ConfigDict(from_attributes=True)