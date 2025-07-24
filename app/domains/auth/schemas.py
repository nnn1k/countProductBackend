from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    login: str
    password: str


class UserRegister(BaseModel):
    nickname: str
    email: EmailStr
    password: str
