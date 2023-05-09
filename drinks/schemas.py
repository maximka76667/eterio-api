from typing import List, Dict
from drinks.models import Drink
from pydantic import BaseModel


class DrinkInDB(Drink):
    id: str


class DrinkOut(BaseModel):
    name: str
    img: str
    code: str
    ingredients: Dict[str, int]
    extra: List[str]
    description: str
    is_community: bool = False


class DrinkOutDB(DrinkOut):
    id: str


class DrinkIn(BaseModel):
    name: str
    img: str
    code: str
    ingredients: Dict[str, int]
    extra: List[str]
    description: str
    is_community: bool = False
