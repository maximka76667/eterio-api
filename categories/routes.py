from fastapi import APIRouter, Depends, HTTPException
from firebase_admin import firestore
from fastapi.encoders import jsonable_encoder
from typing import List

from categories.models import CategoryInDb

router = APIRouter()


@router.get("/", response_model=List[CategoryInDb])
async def get_categories(db: firestore.client = Depends()):
    categories = db.collection("categories").stream()
    categories_list = []
    for category in categories:
        category_data = category.to_dict()
        category_out_db = CategoryInDb(id=category.id, **category_data)
        categories_list.append(category_out_db)
    return categories_list
