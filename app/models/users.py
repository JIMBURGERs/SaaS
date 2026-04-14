from sqlalchemy import Integer, String, Date, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date
from app.db import Base


class User(Base):
    __tablename__ = "users"

    #PK
    UserID: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)

    #Personal Info
    Email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    Password: Mapped[str | None] = mapped_column(String, nullable=True)
    UserName: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    FirstName: Mapped[str] = mapped_column(String, nullable=False)
    LastName: Mapped[str] = mapped_column(String, nullable=False)
    BirthDate: Mapped[date | None] = mapped_column(Date, nullable=True)
    Phone: Mapped[str | None] = mapped_column(String, nullable=True)

    #Account Status
    CreatedAt: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    LastLogin: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    IsActive: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    isDeleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    AccountSetup: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)