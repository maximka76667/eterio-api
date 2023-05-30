from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import firestore
from fastapi.encoders import jsonable_encoder
from typing import List

from bottles.models import BottleInDb

router = APIRouter()


@router.get("/", response_model=List[BottleInDb])
async def get_bottles(db: firestore.client = Depends()):
    bottles = db.collection("bottles").stream()
    bottles_list = []
    for bottle in bottles:
        bottle_data = bottle.to_dict()
        bottle_out_db = BottleInDb(id=bottle.id, **bottle_data)
        bottles_list.append(bottle_out_db)
    return bottles_list
