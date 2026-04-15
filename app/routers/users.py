from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import get_db
from app.models.users import User

router = APIRouter(prefix="/users", tags=["Users"])


#Get
@router.get("/")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()

#Get ID
@router.get("/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.UserID == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

#Post
@router.post("/")
async def create_user(data: dict, db: AsyncSession = Depends(get_db)):
    user = User(**data)

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user

#Put
@router.put("/{user_id}")
async def update_user(user_id: int, data: dict, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.UserID == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in data.items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)

    return user

#Patch
@router.patch("/{user_id}")
async def patch_user(user_id: int, data: dict, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.UserID == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in data.items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)

    return user

#Delete
@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.UserID == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()

    return {"message": "deleted"}