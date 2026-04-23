from datetime import datetime, timedelta, timezone
import random

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.auth_codes import AuthCode


CODE_EXPIRE_MINUTES = 10


def generate_code(length: int = 6) -> str:
    return "".join(str(random.randint(0, 9)) for _ in range(length))


async def create_auth_code(
    db: AsyncSession,
    *,
    user_id: int,
    code_type: str,
    target: str | None = None,
):
    code = generate_code()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=CODE_EXPIRE_MINUTES)

    auth_code = AuthCode(
        UserID=user_id,
        Code=code,
        CodeType=code_type,
        Target=target,
        IsUsed=False,
        ExpiresAt=expires_at,
    )

    db.add(auth_code)
    await db.commit()
    await db.refresh(auth_code)
    return auth_code


async def get_valid_auth_code(
    db: AsyncSession,
    *,
    user_id: int,
    code_type: str,
    code: str,
):
    now = datetime.now(timezone.utc)

    result = await db.execute(
        select(AuthCode)
        .where(
            AuthCode.UserID == user_id,
            AuthCode.CodeType == code_type,
            AuthCode.Code == code,
            AuthCode.IsUsed == False,
            AuthCode.ExpiresAt > now,
        )
        .order_by(AuthCode.CreatedAt.desc())
    )

    return result.scalars().first()


async def mark_auth_code_used(
    db: AsyncSession,
    auth_code: AuthCode,
):
    auth_code.IsUsed = True
    auth_code.UsedAt = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(auth_code)
    return auth_code