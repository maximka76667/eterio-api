import uvicorn
from fastapi import FastAPI, Depends, Request
from pydantic import BaseModel
from google.cloud import firestore
import os
from firebase_admin import credentials, firestore, initialize_app
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from users.schemas import UserInDb

from users.auth import router as auth_router
from users.routes import router as users_router
from drinks.routes import router as drinks_router


# Create a Firebase Admin SDK credentials object
cred = credentials.Certificate(
    "alcopedia-14413-firebase-adminsdk-zanl0-a158742791.json"
)

initialize_app(cred)
app = FastAPI()

bearer_scheme = HTTPBearer()


# Define get_current_user dependency
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> Optional[UserInDb]:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
        user_email = payload.get("email")
        user_name = payload.get("name")
        user_favourite_drinks = payload.get("favourite_drinks", [])
        if not user_id or not user_email or not user_name:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        return UserInDb(
            id=user_id,
            email=user_email,
            name=user_name,
            password="",
            favourite_drinks=user_favourite_drinks,
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


# Define authentication middleware
async def auth_middleware(request: Request, user: UserInDb = Depends(get_current_user)):
    request.state.user = user


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(drinks_router, prefix="/drinks", tags=["drinks"])
