from pydantic import BaseModel
from typing import List


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


class UserInDb(BaseModel):
    id: str
    email: str
    name: str
    password: str
    favourite_drinks: List[str] = []


class User(BaseModel):
    id: str
    email: str
    name: str
    favourite_drinks: List[str] = []
