from pydantic import BaseModel


class UserLogin(BaseModel):
    login: str
    password: str


class UserRegister(BaseModel):
    nickname: str
    email: str
    password: str
