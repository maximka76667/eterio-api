import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from google.cloud import firestore
import os
from firebase_admin import credentials, firestore, initialize_app

from users.routes import router as user_router

# Create a Firebase Admin SDK credentials object
cred = credentials.Certificate(
    "alcopedia-14413-firebase-adminsdk-zanl0-a158742791.json"
)

initialize_app(cred)
app = FastAPI()


app.include_router(user_router, prefix="/users", tags=["users"])

def start():
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    print("Server started")
