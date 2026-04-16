from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    Email: EmailStr
    UserName: str = Field(..., max_length=50)
    FirstName: str = Field(..., max_length=100)
    LastName: str = Field(..., max_length=100)
    BirthDate: date
    Phone: Optional[str] = None


class UserCreate(UserBase):
    Password: Optional[str] = Field(None, min_length=6, max_length=100)
    AuthProvider: str = "local"


class UserUpdate(BaseModel):
    UserName: Optional[str] = Field(None, max_length=50)
    FirstName: Optional[str] = Field(None, max_length=100)
    LastName: Optional[str] = Field(None, max_length=100)
    BirthDate: Optional[date] = None
    Phone: Optional[str] = None
    ProfilePhotoUrl: Optional[str] = None
    AccountSetup: Optional[bool] = None


class UserResponse(BaseModel):
    UserID: int
    Email: EmailStr
    UserName: str
    FirstName: str
    LastName: str
    BirthDate: date
    Phone: Optional[str] = None

    AuthProvider: str

    EmailVerified: bool
    PhoneVerified: bool
    SchoolVerified: bool
    IdentityVerified: bool

    ProfilePhotoUrl: Optional[str] = None
    ProfilePhotoStatus: str
    VerificationStatus: str
    AccountStatus: str

    AccountSetup: bool
    IsActive: bool
    IsDeleted: bool

    CreatedAt: datetime
    UpdatedAt: datetime
    LastLoginAt: Optional[datetime] = None

    class Config:
        from_attributes = True