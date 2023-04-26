from fastapi import APIRouter, Depends
from drinks.models import Drink
from drinks.schemas import DrinkIn, DrinkInDB, DrinkOut, DrinkOutDB
from typing import List, Dict
from firebase_admin import firestore
from fastapi.encoders import jsonable_encoder


router = APIRouter()


@router.post("/", response_model=DrinkOutDB)
async def create_drink(drink: DrinkIn, db: firestore.client = Depends()):
    doc_ref = db.collection("drinks").document()
    doc_ref.set(jsonable_encoder(drink))
    drink_in_db = DrinkInDB(**drink.dict(), id=doc_ref.id)
    return drink_in_db


@router.get("/{drink_id}", response_model=DrinkOutDB)
async def get_drink(drink_id: str, db: firestore.client = Depends()):
    doc_ref = db.collection("drinks").document(drink_id)
    drink = doc_ref.get()
    if drink.exists:
        drink_data = drink.to_dict()
        drink_out_db = DrinkOutDB(id=drink_id, **drink_data)
        return drink_out_db
    else:
        raise HTTPException(status_code=404, detail="Drink not found")


@router.get("/", response_model=List[DrinkOutDB])
async def get_drinks(db: firestore.client = Depends()):
    drinks = db.collection("drinks").stream()
    drinks_list = []
    for drink in drinks:
        drink_data = drink.to_dict()
        drink_out_db = DrinkOutDB(**drink_data, id=drink.id)
        drinks_list.append(drink_out_db)
    return drinks_list


@router.put("/{drink_id}", response_model=DrinkOutDB)
async def update_drink(drink_id: str, drink: DrinkIn, db: firestore.client = Depends()):
    doc_ref = db.collection("drinks").document(drink_id)
    if doc_ref.get().exists:
        doc_ref.update(jsonable_encoder(drink))
        drink_in_db = DrinkInDB(**drink.dict(), id=drink_id)
        return drink_in_db
    else:
        raise HTTPException(status_code=404, detail="Drink not found")


@router.delete("/{drink_id}")
async def delete_drink(drink_id: str, db: firestore.client = Depends()):
    doc_ref = db.collection("drinks").document(drink_id)
    if doc_ref.get().exists:
        doc_ref.delete()
        return {"message": "Drink deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Drink not found")
