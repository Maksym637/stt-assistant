from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    auth0_id: str


class UserResponse(UserBase):
    id: int
    auth0_id: str

    class Config:
        orm_mode = True
