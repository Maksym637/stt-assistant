from pydantic import BaseModel, EmailStr


class Auth0Payload(BaseModel):
    sub: str
    email: EmailStr
