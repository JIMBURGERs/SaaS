from sqlalchemy import Boolean, Column, Date, DateTime, BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date
from sqlalchemy.sql import func
from app.db import Base


class User(Base):
    __tablename__ = "users"

    UserID = Column(BigInteger, primary_key=True, index=True)
    Email = Column(String(255), unique=True, nullable=False, index=True)
    PasswordHash = Column(String(255), nullable=True)  # OAuth user can be NULL
    UserName = Column(String(50), unique=True, nullable=False, index=True)
    FirstName = Column(String(100), nullable=False)
    LastName = Column(String(100), nullable=False)
    BirthDate = Column(Date, nullable=False)
    Phone = Column(String(30), nullable=True)

    AuthProvider = Column(String(30), nullable=False, default="local") #Login path

    EmailVerified = Column(Boolean, nullable=False, default=False)
    PhoneVerified = Column(Boolean, nullable=False, default=False)
    SchoolVerified = Column(Boolean, nullable=False, default=False)
    IdentityVerified = Column(Boolean, nullable=False, default=False)

    ProfilePhotoUrl = Column(String(500), nullable=True)
    ProfilePhotoStatus = Column(String(30), nullable=False, default="pending")
    # pending, approved, rejected, manual_review

    VerificationStatus = Column(String(30), nullable=False, default="unverified")
    # unverified, pending, manual_review, verified, rejected

    AccountStatus = Column(String(30), nullable=False, default="pending_verification")
    # pending_verification, active, restricted, suspended, deleted

    AccountSetup = Column(Boolean, nullable=False, default=False)
    IsActive = Column(Boolean, nullable=False, default=True)
    IsDeleted = Column(Boolean, nullable=False, default=False)

    CreatedAt = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    UpdatedAt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    LastLoginAt = Column(DateTime(timezone=True), nullable=True)