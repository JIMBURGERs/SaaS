from sqlalchemy import Boolean, Column, DateTime, BigInteger, ForeignKey, String
from sqlalchemy.sql import func
from app.db import Base


class AuthCode(Base):
    __tablename__ = "auth_codes"

    AuthCodeID = Column(BigInteger, primary_key=True, index=True)
    UserID = Column(BigInteger, ForeignKey("users.UserID"), nullable=False, index=True)
    Code = Column(String(10), nullable=False, index=True)
    CodeType = Column(String(30), nullable=False, index=True)
    Target = Column(String(255), nullable=True)
    IsUsed = Column(Boolean, nullable=False, default=False)
    ExpiresAt = Column(DateTime(timezone=True), nullable=False)
    CreatedAt = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    UsedAt = Column(DateTime(timezone=True), nullable=True)