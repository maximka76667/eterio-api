from pydantic import BaseModel
from typing import List, Dict


class Bottle(BaseModel):
    name: str
    img: str


class BottleInDb(Bottle):
    id: str
