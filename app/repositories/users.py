from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User
from app.schemas.users import UserCreate, UserUpdate

async def get_users(db: AsyncSession):
    result = await db.execute(
        select(User).where(User.IsDeleted == False)
    )
    return result.scalars().all()


async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(User).where(
            User.UserID == user_id,
            User.IsDeleted == False
        )
    )
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(
        select(User).where(
            User.Email == email,
            User.IsDeleted == False
        )
    )
    return result.scalars().first()


async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(
        select(User).where(
            User.UserName == username,
            User.IsDeleted == False
        )
    )
    return result.scalars().first()


async def get_user_by_phone(db: AsyncSession, phone: str):
    result = await db.execute(
        select(User).where(
            User.Phone == phone,
            User.IsDeleted == False
        )
    )
    return result.scalars().first()


async def create_user(
    db: AsyncSession,
    user_data: UserCreate,
    password_hash: str | None = None
):
    user = User(
        Email=user_data.Email,
        PasswordHash=password_hash,
        UserName=user_data.UserName,
        FirstName=user_data.FirstName,
        LastName=user_data.LastName,
        BirthDate=user_data.BirthDate,
        Phone=user_data.Phone,
        AuthProvider=user_data.AuthProvider,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(db: AsyncSession, user: User, user_data: UserUpdate):
    update_data = user_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user


async def soft_delete_user(db: AsyncSession, user: User):
    user.IsDeleted = True
    user.IsActive = False
    user.AccountStatus = "deleted"

    await db.commit()
    await db.refresh(user)
    return user