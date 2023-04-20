from pydantic import BaseModel


class UserModel(BaseModel):
    id: str
    email: str
    name: str
    password: str
