from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    EmailVerificationRequest,
    PhoneVerificationRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    AuthMessageResponse,
    TokenResponse,
)
from app.repositories.users import (
    get_user_by_email,
    get_user_by_username,
    get_user_by_phone,
)
from app.repositories.auth import (
    register_user,
    authenticate_user,
    verify_user_email,
    verify_user_phone,
    update_user_password,
    update_last_login,
    can_user_interact,
)
from app.repositories.auth_codes import (
    create_auth_code,
    get_valid_auth_code,
    mark_auth_code_used,
)
from app.utils.hashing import hash_password, verify_password
from app.utils.jwt import create_access_token, create_password_reset_token, decode_token
from app.utils.email import (
    send_registration_email,
    send_email_verification_email,
    send_password_reset_email,
    send_password_changed_email,
    send_login_alert_email,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    existing_email = get_user_by_email(db, request.Email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    existing_username = get_user_by_username(db, request.UserName)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    if request.Phone:
        existing_phone = get_user_by_phone(db, request.Phone)
        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone already exists"
            )

    password_hash = hash_password(request.Password)

    user = register_user(
        db,
        email=request.Email,
        username=request.UserName,
        first_name=request.FirstName,
        last_name=request.LastName,
        birth_date=request.BirthDate,
        phone=request.Phone,
        password_hash=password_hash,
        auth_provider=request.AuthProvider,
    )

    verification_code = create_auth_code(
        db,
        user_id=user.UserID,
        code_type="email_verification",
        target=user.Email,
    )

    send_registration_email(user.Email, user.FirstName)
    send_email_verification_email(user.Email, user.FirstName, verification_code.Code)

    access_token = create_access_token(user.UserID)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user,
        "permissions": {
            "can_view": True,
            "can_interact": can_user_interact(user),
        },
    }


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, request.Email)

    if not user or not user.PasswordHash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(request.Password, user.PasswordHash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if user.AccountStatus == "deleted" or user.IsDeleted:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account has been deleted"
        )

    if user.AccountStatus == "suspended":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is suspended"
        )

    if not user.IsActive:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )

    access_token = create_access_token(user.UserID)
    update_last_login(db, user)
    send_login_alert_email(user.Email, user.FirstName)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user,
        "permissions": {
            "can_view": True,
            "can_interact": can_user_interact(user),
        },
    }


@router.post("/verify-email", response_model=AuthMessageResponse)
def verify_email(request: EmailVerificationRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, request.Email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    auth_code = get_valid_auth_code(
        db,
        user_id=user.UserID,
        code_type="email_verification",
        code=request.Code,
    )
    if not auth_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification code"
        )

    mark_auth_code_used(db, auth_code)
    verify_user_email(db, user)

    return {"message": "Email verified successfully"}


@router.post("/verify-phone", response_model=AuthMessageResponse)
def verify_phone(request: PhoneVerificationRequest, db: Session = Depends(get_db)):
    user = get_user_by_phone(db, request.Phone)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    auth_code = get_valid_auth_code(
        db,
        user_id=user.UserID,
        code_type="phone_verification",
        code=request.Code,
    )
    if not auth_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification code"
        )

    mark_auth_code_used(db, auth_code)
    verify_user_phone(db, user)

    return {"message": "Phone verified successfully"}


@router.post("/forgot-password", response_model=AuthMessageResponse)
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, request.Email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user.IsDeleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Deleted account cannot reset password"
        )

    reset_token = create_password_reset_token(user.UserID)
    reset_link = f"http://localhost:3000/reset-password?token={reset_token}"
    send_password_reset_email(user.Email, reset_link)

    return {"message": "Password reset email sent"}


@router.post("/reset-password", response_model=AuthMessageResponse)
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        payload = decode_token(request.Token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )

    if payload.get("type") != "password_reset":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reset token type"
        )

    user_id = int(payload["sub"])

    from app.repositories.users import get_user_by_id
    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not user.PasswordHash and user.AuthProvider != "local":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password reset is not available for this account"
        )

    new_password_hash = hash_password(request.NewPassword)
    update_user_password(db, user, new_password_hash)
    send_password_changed_email(user.Email)

    return {"message": "Password reset successfully"}