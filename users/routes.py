from fastapi import APIRouter, Depends
from fastapi import status
from firebase_admin import firestore
from fastapi.responses import JSONResponse
from fastapi import HTTPException


from users.models import UserModel
from users.schemas import User, UserCreate, UserInDb

router = APIRouter()


@router.get("/", response_model=list[User])
async def get_users(db: firestore.client = Depends()):
    users = db.collection("users").stream()
    result = []
    for user in users:
        data = user.to_dict()
        result.append(User(id=user.id, email=data["email"], name=data["name"]))
    return result


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: firestore.client = Depends()):
    doc_ref = db.collection("users").document()
    doc_ref.set(user.dict())
    return doc_ref.get().to_dict()


@router.get("/{user_id}", response_model=User)
def get_user(user_id: str, db: firestore.client = Depends()):
    doc_ref = db.collection("users").document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        return User(id=user_id, **doc.to_dict())
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.put("/{user_id}", response_model=User)
def update_user(user_id: str, user: UserCreate, db: firestore.client = Depends()):
    doc_ref = db.collection("users").document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.update(user.dict())
        return User(id=user_id, **doc.to_dict())
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.delete("/{user_id}", status_code=200, response_model=User)
def delete_user(user_id: str, db: firestore.client = Depends()):
    doc_ref = db.collection("users").document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.delete()
        return User(id=user_id, **doc.to_dict())
    else:
        raise HTTPException(status_code=404, detail="User not found")
