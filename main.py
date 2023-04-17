from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from google.cloud import firestore
import os
from firebase_admin import credentials, firestore, initialize_app

# Create a Firebase Admin SDK credentials object
cred = credentials.Certificate(
    "alcopedia-14413-firebase-adminsdk-zanl0-a158742791.json"
)

initialize_app(cred)
db = firestore.client()
app = FastAPI()


class User(BaseModel):
    name: str
    age: int


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    doc_ref = db.collection("users").document()
    doc_ref.set(user.dict())
    return JSONResponse(content={"user_id": doc_ref.id})


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: str):
    doc_ref = db.collection("users").document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        return User(**doc.to_dict())
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: str, user: User):
    doc_ref = db.collection("users").document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.update(user.dict())
        return User(**doc.to_dict())
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    doc_ref = db.collection("users").document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        doc_ref.delete()
        return JSONResponse(content={"detail": "User deleted"})
    else:
        raise HTTPException(status_code=404, detail="User not found")


print("Server started")
