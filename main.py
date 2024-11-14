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

# Limiter
from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from decouple import config

# Create a Firebase Admin SDK credentials object
cred = credentials.Certificate(
    {
        "type": "service_account",
        "project_id": config("FIREBASE_PROJECT_ID"),
        "private_key_id": config("PRIVATE_KEY_ID"),
        "private_key": config("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
        "client_email": config("FIREBASE_CLIENT_EMAIL"),
        "client_id": config("CLIENT_ID"),
        "auth_uri": config("AUTH_URI"),
        "token_uri": config("TOKEN_URI"),
        "auth_provider_x509_cert_url": config("AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": config("CLIENT_X509_CERT_URL"),
        "universe_domain": "googleapis.com",
    }
)

initialize_app(cred)

# Limiter
limiter = Limiter(key_func=get_remote_address, application_limits=["40/5seconds"])

# Initialize App
app = FastAPI()

bearer_scheme = HTTPBearer()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SlowAPIMiddleware) ## Rate-limit all request

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(categories_router, prefix="/categories", tags=["categories"])
app.include_router(bottles_router, prefix="/bottles", tags=["bottles"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(drinks_router, prefix="/drinks", tags=["drinks"])