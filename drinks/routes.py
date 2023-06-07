from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import firestore
from fastapi.encoders import jsonable_encoder
from typing import List

from drinks.models import Drink, DrinkInDb
from users.auth import require_authentication

from users.models import UserInDb

router = APIRouter()


@router.post("/", response_model=DrinkInDb)
async def create_drink(drink: Drink, db: firestore.client = Depends()):
    doc_ref = db.collection("drinks").document()
    doc_ref.set(jsonable_encoder(drink))

    drink_data = drink.dict()

    if drink_data["name"] == "" and drink_data["code"] == "":
        raise HTTPException(status_code=400, detail="Name and code are required")

    drink_in_db = DrinkInDb(**drink.dict(), id=doc_ref.id)
    return drink_in_db


@router.get("/{drink_id}", response_model=DrinkInDb)
async def get_drink(drink_id: str, db: firestore.client = Depends()):
    doc_ref = db.collection("drinks").document(drink_id)

    drink = doc_ref.get()
    if drink.exists:
        drink_data = drink.to_dict()
        drink_out_db = DrinkInDb(id=drink_id, **drink_data)
        return drink_out_db
    else:
        raise HTTPException(status_code=404, detail="Drink not found")


@router.get("/", response_model=List[DrinkInDb])
async def get_drinks(db: firestore.client = Depends()):
    drinks = db.collection("drinks").stream()
    drinks_list = []
    for drink in drinks:
        drink_data = drink.to_dict()
        drink_out_db = DrinkInDb(**drink_data, id=drink.id)
        drinks_list.append(drink_out_db)
    return drinks_list


@router.put("/{drink_id}", response_model=DrinkInDb)
async def update_drink(drink_id: str, drink: Drink, db: firestore.client = Depends()):
    doc_ref = db.collection("drinks").document(drink_id)
    if doc_ref.get().exists:
        doc_ref.update(jsonable_encoder(drink))
        drink_in_db = DrinkInDb(**drink.dict(), id=drink_id)
        return drink_in_db
    else:
        raise HTTPException(status_code=404, detail="Drink not found")


@router.delete("/{drink_id}")
async def delete_drink(
    drink_id: str,
    db: firestore.client = Depends(),
    current_user: UserInDb = Depends(require_authentication),
):
    doc_ref = db.collection("drinks").document(drink_id)

    drink = doc_ref.get().to_dict()

    if drink.get("author") != current_user.id:
        raise HTTPException(status_code=403, detail="Current user is not an author")

    if doc_ref.get().exists:
        doc_ref.delete()
        return {"message": "Drink deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Drink not found")


# Add fav
@router.put("/favs/{drink_id}")
async def add_fav(
    drink_id: str,
    db: firestore.client = Depends(),
    current_user: UserInDb = Depends(require_authentication),
):
    user_id = current_user.dict().get("id")

    drink_ref = db.collection("drinks").document(drink_id)
    drink_doc = drink_ref.get()

    if not drink_doc.exists:
        raise HTTPException(status_code=404, detail="Drink not found")

    drink_data = drink_doc.to_dict()

    if user_id not in drink_data["favorites"]:
        drink_data["favorites"].append(user_id)
        drink_ref.update({"favorites": drink_data["favorites"]})

    return DrinkInDb(id=drink_id, **drink_ref.get().to_dict())


@router.delete("/favs/{drink_id}")
async def delete_fav(
    drink_id: str,
    db: firestore.client = Depends(),
    current_user: UserInDb = Depends(require_authentication),
):
    user_id = current_user.dict().get("id")

    drink_ref = db.collection("drinks").document(drink_id)
    drink_doc = drink_ref.get()

    if not drink_doc.exists:
        raise HTTPException(status_code=404, detail="Drink not found")

    drink_data = drink_doc.to_dict()
    if user_id in drink_data["favorites"]:
        drink_data["favorites"].remove(user_id)
        drink_ref.update({"favorites": drink_data["favorites"]})

    return DrinkInDb(id=drink_id, **drink_ref.get().to_dict())
