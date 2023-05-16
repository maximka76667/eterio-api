from pydantic import BaseModel
from typing import List, Dict


class Category(BaseModel):
    name: str


class CategoryInDb(Category):
    id: str
