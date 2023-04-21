from fastapi import APIRouter, Depends
from fastapi import status
from firebase_admin import firestore
from fastapi.responses import JSONResponse
from fastapi import HTTPException
import bcrypt

from users.models import UserModel
from users.schemas import User, UserCreate, UserInDb, UserUpdate

router = APIRouter()


# Get all users
@router.get("/", response_model=list[User])
async def get_users(db: firestore.client = Depends()):
    users = db.collection("users").stream()
    result = []
    for user in users:
        user_data = user.to_dict()
        result.append(
            User(
                id=user.id,
                email=user_data["email"],
                name=user_data["name"],
                favourite_drinks=user_data["favourite_drinks"],
            )
        )
    return result


# Create user
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: firestore.client = Depends()):
    raw_user = user.dict()
    email = raw_user["email"]

    user_doc_ref = db.collection("users")
    user_doc = user_doc_ref.document()
    user = user_doc.get()

    if len(user_doc_ref.where("email", "==", email).get()) != 0:
        raise HTTPException(status_code=401, detail="Email already exists")

    # Encrypt password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(raw_user["password"].encode("utf-8"), salt)

    new_user = UserInDb(
        id=user.id,
        email=raw_user["email"],
        name=raw_user["name"],
        password=hashed_password,
        favourite_drinks=[],
    )

    user_doc.set(new_user.dict())
    return user_doc.get().to_dict()


# Get user by id
@router.get("/{user_id}", response_model=User)
def get_user(user_id: str, db: firestore.client = Depends()):
    doc_ref = db.collection("users").document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        return User(**doc.to_dict())
    else:
        raise HTTPException(status_code=404, detail="User not found")


# Update user
@router.put("/{user_id}", response_model=User)
def update_user(user_id: str, user: UserUpdate, db: firestore.client = Depends()):
    users_ref = db.collection("users")
    user_update_doc = users_ref.document(user_id)
    user_update = user_update_doc.get()

    if user_update.exists:
        email = user.dict()["email"]

        if user_update.to_dict().get("email") != email:
            if len(users_ref.where("email", "==", email).get()) != 0:
                raise HTTPException(status_code=401, detail="Email already exists")

        user_update_doc.update(user.dict())

        updated_user = user_update_doc.get()
        return User(**updated_user.to_dict())
    else:
        raise HTTPException(status_code=404, detail="User not found")


# Delete user
@router.delete("/{user_id}", status_code=200, response_model=User)
def delete_user(user_id: str, db: firestore.client = Depends()):
    doc_ref = db.collection("users").document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.delete()
        return User(**doc.to_dict())
    else:
        raise HTTPException(status_code=404, detail="User not found")
