import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from google.cloud import firestore
import os
from firebase_admin import credentials, firestore, initialize_app
from fastapi.middleware.cors import CORSMiddleware

from users.routes import router as users_router
from drinks.routes import router as drinks_router


# Create a Firebase Admin SDK credentials object
cred = credentials.Certificate(
    "alcopedia-14413-firebase-adminsdk-zanl0-a158742791.json"
)

initialize_app(cred)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(drinks_router, prefix="/drinks", tags=["drinks"])
