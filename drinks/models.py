from pydantic import BaseModel
from typing import List, Dict


class Drink(BaseModel):
    name: str
    img: str = "https://www.uchicagomedicine.org/-/media/images/ucmc/forefront/channel-pages/health-and-wellness/carbonated-water-universal-832x469.jpg"
    code: str
    ingredients: Dict[str, int]
    extra: List[str]
    description: str
    is_community: bool = False
    favorites = []
    author: str
    category: str


class DrinkInDb(Drink):
    id: str
