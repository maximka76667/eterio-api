from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    name: str
    password: str

class UserUpdate(BaseModel):
    email: str
    name: str

class UserInDb(UserCreate):
    id: str


class User(BaseModel):
    id: str
    email: str
    name: str
