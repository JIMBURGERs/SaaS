from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.users import User


def register_user(
    db: Session,
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
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str):
    return db.query(User).filter(
        User.Email == email,
        User.IsDeleted == False
    ).first()


def verify_user_email(db: Session, user: User):
    user.EmailVerified = True

    if user.EmailVerified or user.PhoneVerified or user.IdentityVerified or user.SchoolVerified:
        user.VerificationStatus = "verified"
        user.AccountStatus = "active"
    else:
        user.VerificationStatus = "pending"

    db.commit()
    db.refresh(user)
    return user


def verify_user_phone(db: Session, user: User):
    user.PhoneVerified = True

    if user.EmailVerified or user.PhoneVerified or user.IdentityVerified or user.SchoolVerified:
        user.VerificationStatus = "verified"
        user.AccountStatus = "active"
    else:
        user.VerificationStatus = "pending"

    db.commit()
    db.refresh(user)
    return user


def update_user_password(db: Session, user: User, password_hash: str):
    user.PasswordHash = password_hash
    db.commit()
    db.refresh(user)
    return user


def update_last_login(db: Session, user: User):
    user.LastLoginAt = datetime.now(timezone.utc)
    db.commit()
    db.refresh(user)
    return user


def can_user_interact(user: User) -> bool:
    return (
        user.IsActive
        and not user.IsDeleted
        and user.AccountStatus == "active"
    )