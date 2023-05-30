import uvicorn
from fastapi import FastAPI, Depends, Request
from pydantic import BaseModel
from google.cloud import firestore
import os
from firebase_admin import credentials, firestore, initialize_app
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from users.models import UserInDb

from users.auth import router as auth_router
from users.routes import router as users_router
from drinks.routes import router as drinks_router
from categories.routes import router as categories_router
from bottles.routes import router as bottles_router


# Create a Firebase Admin SDK credentials object
cred = credentials.Certificate(
    "alcopedia-14413-firebase-adminsdk-zanl0-a158742791.json"
)

initialize_app(cred)
app = FastAPI()

bearer_scheme = HTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(categories_router, prefix="/categories", tags=["categories"])
app.include_router(bottles_router, prefix="/bottles", tags=["bottles"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(drinks_router, prefix="/drinks", tags=["drinks"])
