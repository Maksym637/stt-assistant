from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException, status

from core.db_session import get_db
from core.auth import get_current_account

from schemas.auth import Auth0Payload
from schemas.user import UserCreate, UserResponse

from crud.user import get_user_by_id, create_user


router = APIRouter()


@router.get(
    "/me",
    response_model=UserResponse,
    description="Returns the authenticated user's account details",
    status_code=status.HTTP_200_OK,
    responses={
        401: {"description": "Not authenticated"},
        404: {"description": "User's account not found"},
    },
)
def get_authenticated_user(
    db: Session = Depends(get_db),
    auth0_user: Auth0Payload = Depends(get_current_account),
):
    db_user = get_user_by_id(db, auth0_user.sub)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User's account not found"
        )

    return db_user


@router.post(
    "/create",
    response_model=UserResponse,
    description="Create a new user for the authenticated user if one does not exist",
    status_code=status.HTTP_200_OK,
    responses={
        "401": {"description": "Not authenticated"},
        "409": {"description": "User's account already exists"},
    },
)
def create_authenticated_user_account(
    db: Session = Depends(get_db),
    auth0_user: Auth0Payload = Depends(get_current_account),
):
    db_user = get_user_by_id(db, auth0_user.sub)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User's account already exists"
        )

    new_user = UserCreate(email=auth0_user.email, auth0_id=auth0_user.sub)
    db_user = create_user(db, new_user)

    return db_user
