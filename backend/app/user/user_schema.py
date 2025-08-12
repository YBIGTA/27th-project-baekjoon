from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    email: EmailStr
    password: str
    username: str

class UserDB(User):
    """
    내부 저장소용 모델 (salt 포함). API 스키마에는 노출하지 않습니다.
    """
    salt: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    email: EmailStr
    current_password: str
    new_password: str

class UserDeleteRequest(BaseModel):
    email: EmailStr
    password: str

class MessageResponse(BaseModel):
    message: str


class UserPublic(BaseModel):
    email: EmailStr
    username: str


class LoginResponse(BaseModel):
    user: UserPublic
    access_token: str
    token_type: str = "bearer"

