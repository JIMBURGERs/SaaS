from datetime import date
from pydantic import BaseModel, EmailStr, Field

from app.schemas.users import UserResponse


class RegisterRequest(BaseModel):
    Email: EmailStr
    UserName: str = Field(..., max_length=50)
    FirstName: str = Field(..., max_length=100)
    LastName: str = Field(..., max_length=100)
    BirthDate: date
    Phone: str | None = Field(default=None, max_length=30)
    Password: str = Field(..., min_length=6, max_length=100)
    AuthProvider: str = "local"

    model_config = {
        "json_schema_extra": {
            "example": {
                "Email": "joon@gmail.com",
                "UserName": "testuser",
                "FirstName": "Joon",
                "LastName": "Hong",
                "BirthDate": "2003-04-23",
                "Phone": "111-111-1111",
                "Password": "test1234!",
                "AuthProvider": "local"
            }
        }
    }


class LoginRequest(BaseModel):
    Email: EmailStr
    Password: str = Field(..., min_length=6, max_length=100)

    model_config = {
        "json_schema_extra": {
            "example": {
                "Email": "joon@gmail.com",
                "Password": "test1234!"
            }
        }
    }


class EmailVerificationRequest(BaseModel):
    Email: EmailStr
    Code: str = Field(..., min_length=4, max_length=10)

    model_config = {
        "json_schema_extra": {
            "example": {
                "Email": "joon@gmail.com",
                "Code": "123456"
            }
        }
    }


class PhoneVerificationRequest(BaseModel):
    Phone: str = Field(..., max_length=30)
    Code: str = Field(..., min_length=4, max_length=10)

    model_config = {
        "json_schema_extra": {
            "example": {
                "Phone": "111-111-1111",
                "Code": "123456"
            }
        }
    }


class ForgotPasswordRequest(BaseModel):
    Email: EmailStr

    model_config = {
        "json_schema_extra": {
            "example": {
                "Email": "joon@gmail.com"
            }
        }
    }


class ResetPasswordRequest(BaseModel):
    Token: str
    NewPassword: str = Field(..., min_length=6, max_length=100)

    model_config = {
        "json_schema_extra": {
            "example": {
                "Token": "your.password.reset.jwt",
                "NewPassword": "newpass1234!"
            }
        }
    }


class AuthMessageResponse(BaseModel):
    message: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "Success"
            }
        }
    }


class PermissionsResponse(BaseModel):
    can_view: bool
    can_interact: bool

    model_config = {
        "json_schema_extra": {
            "example": {
                "can_view": True,
                "can_interact": False
            }
        }
    }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
    permissions: PermissionsResponse

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "your.jwt.token",
                "token_type": "bearer",
                "user": {
                    "UserID": 1,
                    "Email": "joon@gmail.com",
                    "UserName": "testuser",
                    "FirstName": "Joon",
                    "LastName": "Hong",
                    "BirthDate": "2003-04-23",
                    "Phone": "111-111-1111",
                    "AuthProvider": "local",
                    "EmailVerified": False,
                    "PhoneVerified": False,
                    "SchoolVerified": False,
                    "IdentityVerified": False,
                    "ProfilePhotoUrl": None,
                    "ProfilePhotoStatus": "pending",
                    "VerificationStatus": "unverified",
                    "AccountStatus": "pending_verification",
                    "AccountSetup": False,
                    "IsActive": True,
                    "IsDeleted": False,
                    "CreatedAt": "2026-04-16T10:00:00Z",
                    "UpdatedAt": "2026-04-16T10:00:00Z",
                    "LastLoginAt": "2026-04-20T10:00:00Z"
                },
                "permissions": {
                    "can_view": True,
                    "can_interact": False
                }
            }
        }
    }