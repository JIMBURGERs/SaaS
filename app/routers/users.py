from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.users import UserCreate, UserResponse, UserUpdate
from repositories.users import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    get_user_by_username,
    get_users,
    soft_delete_user,
    update_user,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse])
def read_users(db: Session = Depends(get_db)):
    return get_users(db)


@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_email = get_user_by_email(db, user_data.Email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    existing_username = get_user_by_username(db, user_data.UserName)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    # TODO: replace with real password hashing later
    password_hash = user_data.Password if user_data.Password else None

    return create_user(db, user_data, password_hash=password_hash)


@router.put("/{user_id}", response_model=UserResponse)
def update_existing_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return update_user(db, user, user_data)


@router.delete("/{user_id}", response_model=UserResponse)
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return soft_delete_user(db, user)