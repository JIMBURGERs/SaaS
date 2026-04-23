from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.auth import *
from app.repositories.users import *
from app.repositories.auth import *
from app.repositories.auth_codes import *
from app.utils.hashing import hash_password, verify_password
from app.utils.jwt import create_access_token, create_password_reset_token, decode_token
from app.utils.email import *

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    existing_email = await get_user_by_email(db, request.Email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    existing_username = await get_user_by_username(db, request.UserName)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already exists")

    if request.Phone:
        existing_phone = await get_user_by_phone(db, request.Phone)
        if existing_phone:
            raise HTTPException(status_code=400, detail="Phone already exists")

    password_hash = hash_password(request.Password)

    user = await register_user(
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

    verification_code = await create_auth_code(
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
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, request.Email)

    if not user or not user.PasswordHash:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(request.Password, user.PasswordHash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if user.AccountStatus == "deleted" or user.IsDeleted:
        raise HTTPException(status_code=403, detail="Account has been deleted")

    if user.AccountStatus == "suspended":
        raise HTTPException(status_code=403, detail="Account is suspended")

    if not user.IsActive:
        raise HTTPException(status_code=403, detail="Account is inactive")

    access_token = create_access_token(user.UserID)

    await update_last_login(db, user)
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
async def verify_email(request: EmailVerificationRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, request.Email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    auth_code = await get_valid_auth_code(
        db,
        user_id=user.UserID,
        code_type="email_verification",
        code=request.Code,
    )
    if not auth_code:
        raise HTTPException(status_code=400, detail="Invalid or expired verification code")

    await mark_auth_code_used(db, auth_code)
    await verify_user_email(db, user)

    return {"message": "Email verified successfully"}


@router.post("/verify-phone", response_model=AuthMessageResponse)
async def verify_phone(request: PhoneVerificationRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_phone(db, request.Phone)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    auth_code = await get_valid_auth_code(
        db,
        user_id=user.UserID,
        code_type="phone_verification",
        code=request.Code,
    )
    if not auth_code:
        raise HTTPException(status_code=400, detail="Invalid or expired verification code")

    await mark_auth_code_used(db, auth_code)
    await verify_user_phone(db, user)

    return {"message": "Phone verified successfully"}


@router.post("/forgot-password", response_model=AuthMessageResponse)
async def forgot_password(request: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, request.Email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.IsDeleted:
        raise HTTPException(status_code=400, detail="Deleted account cannot reset password")

    reset_token = create_password_reset_token(user.UserID)
    reset_link = f"http://localhost:3000/reset-password?token={reset_token}"
    send_password_reset_email(user.Email, reset_link)

    return {"message": "Password reset email sent"}


@router.post("/reset-password", response_model=AuthMessageResponse)
async def reset_password(request: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    try:
        payload = decode_token(request.Token)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")

    if payload.get("type") != "password_reset":
        raise HTTPException(status_code=400, detail="Invalid reset token type")

    user_id = int(payload["sub"])

    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.PasswordHash and user.AuthProvider != "local":
        raise HTTPException(status_code=400, detail="Password reset not available")

    new_password_hash = hash_password(request.NewPassword)

    await update_user_password(db, user, new_password_hash)
    send_password_changed_email(user.Email)

    return {"message": "Password reset successfully"}