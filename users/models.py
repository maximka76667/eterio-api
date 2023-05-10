from pydantic import BaseModel
from typing import List

default_avatar = "https://images.unsplash.com/photo-1491528323818-fdd1faba62cc?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"


class UserCreate(BaseModel):
    email: str
    name: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    email: str
    name: str
    avatar: str = default_avatar


class User(BaseModel):
    id: str
    email: str
    name: str
    avatar: str = default_avatar


class UserInDb(User):
    password: str
