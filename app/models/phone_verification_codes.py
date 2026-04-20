from sqlalchemy import Boolean, Column, DateTime, BigInteger, ForeignKey, String
from sqlalchemy.sql import func
from app.db import Base


class PhoneVerificationCode(Base):
    __tablename__ = "phone_verification_codes"

    ID = Column(BigInteger, primary_key=True, index=True)
    UserID = Column(BigInteger, ForeignKey("users.UserID"), nullable=False, index=True)
    Phone = Column(String(30), nullable=False, index=True)
    Code = Column(String(10), nullable=False)
    Purpose = Column(String(30), nullable=False, default="verify_phone")
    IsUsed = Column(Boolean, nullable=False, default=False)
    ExpiresAt = Column(DateTime(timezone=True), nullable=False)
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)