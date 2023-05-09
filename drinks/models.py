from pydantic import BaseModel
from typing import List, Dict


class Drink(BaseModel):
    name: str
    img: str
    code: str
    ingredients: Dict[str, int]
    extra: List[str]
    description: str
    is_community: bool = False
