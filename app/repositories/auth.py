from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User


async def register_user(
    db: AsyncSession,
    *,
    email: str,
    username: str,
    first_name: str,
    last_name: str,
    birth_date,
    phone: str | None,
    password_hash: str,
    auth_provider: str = "local",
):
    user = User(
        Email=email,
        PasswordHash=password_hash,
        UserName=username,
        FirstName=first_name,
        LastName=last_name,
        BirthDate=birth_date,
        Phone=phone,
        AuthProvider=auth_provider,
        EmailVerified=False,
        PhoneVerified=False,
        SchoolVerified=False,
        IdentityVerified=False,
        VerificationStatus="unverified",
        AccountStatus="pending_verification",
        AccountSetup=False,
        IsActive=True,
        IsDeleted=False,
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate_user(db: AsyncSession, email: str):
    result = await db.execute(
        select(User).where(
            User.Email == email,
            User.IsDeleted == False
        )
    )
    return result.scalars().first()


async def verify_user_email(db: AsyncSession, user: User):
    user.EmailVerified = True

    if user.EmailVerified or user.PhoneVerified or user.IdentityVerified or user.SchoolVerified:
        user.VerificationStatus = "verified"
        user.AccountStatus = "active"
    else:
        user.VerificationStatus = "pending"

    await db.commit()
    await db.refresh(user)
    return user


async def verify_user_phone(db: AsyncSession, user: User):
    user.PhoneVerified = True

    if user.EmailVerified or user.PhoneVerified or user.IdentityVerified or user.SchoolVerified:
        user.VerificationStatus = "verified"
        user.AccountStatus = "active"
    else:
        user.VerificationStatus = "pending"

    await db.commit()
    await db.refresh(user)
    return user


async def update_user_password(db: AsyncSession, user: User, password_hash: str):
    user.PasswordHash = password_hash
    await db.commit()
    await db.refresh(user)
    return user


async def update_last_login(db: AsyncSession, user: User):
    user.LastLoginAt = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(user)
    return user


def can_user_interact(user: User) -> bool:
    return (
        user.IsActive
        and not user.IsDeleted
        and user.AccountStatus == "active"
    )