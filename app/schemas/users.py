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

    model_config = {
        "json_schema_extra": {
            "example": {
                "Email": "joon@gmail.com",
                "UserName": "test",
                "FirstName": "test",
                "LastName": "test",
                "BirthDate": "2003-04-23",
                "Phone": "111-111-1111"
            }
        }
    }


class UserCreate(UserBase):
    Password: Optional[str] = Field(None, min_length=6, max_length=100)
    AuthProvider: str = "local"

    model_config = {
        "json_schema_extra": {
            "example": {
                "Email": "joon@gmail.com",
                "UserName": "test",
                "FirstName": "test",
                "LastName": "test",
                "BirthDate": "2003-04-23",
                "Phone": "111-111-1111",
                "Password": "test1234",
                "AuthProvider": "local"
            }
        }
    }


class UserUpdate(BaseModel):
    UserName: Optional[str] = Field(None, max_length=50)
    FirstName: Optional[str] = Field(None, max_length=100)
    LastName: Optional[str] = Field(None, max_length=100)
    BirthDate: Optional[date] = None
    Phone: Optional[str] = None
    ProfilePhotoUrl: Optional[str] = None
    AccountSetup: Optional[bool] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "UserName": "updated_test",
                "FirstName": "Joon",
                "LastName": "Hong",
                "BirthDate": "2003-04-23",
                "Phone": "222-222-2222",
                "ProfilePhotoUrl": "https://example.com/profile.jpg",
                "AccountSetup": True
            }
        }
    }


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

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "UserID": 1,
                "Email": "joon@gmail.com",
                "UserName": "test",
                "FirstName": "test",
                "LastName": "test",
                "BirthDate": "2003-04-23",
                "Phone": "111-111-1111",
                "AuthProvider": "local",
                "EmailVerified": False,
                "PhoneVerified": False,
                "SchoolVerified": False,
                "IdentityVerified": False,
                "ProfilePhotoUrl": "https://example.com/profile.jpg",
                "ProfilePhotoStatus": "pending",
                "VerificationStatus": "unverified",
                "AccountStatus": "pending_verification",
                "AccountSetup": False,
                "IsActive": True,
                "IsDeleted": False,
                "CreatedAt": "2026-04-16T10:00:00Z",
                "UpdatedAt": "2026-04-16T10:00:00Z",
                "LastLoginAt": None
            }
        }
    }