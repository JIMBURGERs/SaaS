from datetime import date, datetime, timezone

from sqlalchemy import Boolean, Date, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class User(Base):
    __tablename__ = "users"

    UserID: Mapped[int] = mapped_column(primary_key=True, index=True)
    Email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    PasswordHash: Mapped[str | None] = mapped_column(String, nullable=True)
    UserName: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    Phone: Mapped[str | None] = mapped_column(String, nullable=True)

    FirstName: Mapped[str] = mapped_column(String, nullable=False)
    LastName: Mapped[str] = mapped_column(String, nullable=False)
    BirthDate: Mapped[date] = mapped_column(Date, nullable=False)
    AuthProvider: Mapped[str] = mapped_column(String, nullable=False, default="local")

    EmailVerified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    PhoneVerified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    SchoolVerified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    IdentityVerified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    ProfilePhotoUrl: Mapped[str | None] = mapped_column(String, nullable=True)
    ProfilePhotoStatus: Mapped[str] = mapped_column(String, nullable=False, default="pending")

    VerificationStatus: Mapped[str] = mapped_column(String, nullable=False, default="unverified")
    AccountStatus: Mapped[str] = mapped_column(String, nullable=False, default="pending_verification")
    AccountSetup: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    IsActive: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    IsDeleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    CreatedAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    UpdatedAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    LastLoginAt: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )