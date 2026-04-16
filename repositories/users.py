from sqlalchemy.orm import Session

from app.models.users import User
from app.schemas.users import UserCreate, UserUpdate


def get_users(db: Session):
    return db.query(User).filter(User.IsDeleted == False).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.UserID == user_id, User.IsDeleted == False).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.Email == email, User.IsDeleted == False).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.UserName == username, User.IsDeleted == False).first()


def create_user(db: Session, user_data: UserCreate, password_hash: str | None = None):
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
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: User, user_data: UserUpdate):
    update_data = user_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def soft_delete_user(db: Session, user: User):
    user.IsDeleted = True
    user.IsActive = False
    user.AccountStatus = "deleted"
    db.commit()
    db.refresh(user)
    return user