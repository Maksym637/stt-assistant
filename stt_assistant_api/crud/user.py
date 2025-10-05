from sqlalchemy.orm import Session

from models.user import User

from schemas.user import UserCreate


def create_user(db: Session, data: UserCreate):
    user = UserCreate(auth0_id=data.auth0_id, email=data.email)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_id(db: Session, auth0_id: str):
    return db.query(User).filter(User.auth0_id == auth0_id).first()
