from fastapi import APIRouter, Depends
from fastapi import status
from typing import Dict, Union
from firebase_admin import firestore
from fastapi.responses import JSONResponse
from fastapi import HTTPException
import bcrypt

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import jwt


from users.models import UserLogin, UserInDb, UserUpdate

router = APIRouter()

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 600


@router.post("/login")
async def login_user(user_data: UserLogin, db: firestore.client = Depends()):
    user_data_dict = user_data.dict()
    user = await authenticate_user(
        user_data_dict["email"], user_data_dict["password"], db
    )

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    user_dict = user.dict()

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_data = {
        "sub": str(user_dict["id"]),
        "exp": datetime.utcnow() + access_token_expires,
    }
    access_token = jwt.encode(access_token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": access_token, "token_type": "bearer"}


async def authenticate_user(
    email: str, password: str, db: firestore.client
) -> Union[UserInDb, None]:
    user = await get_user_by_email(email, db)
    if not user:
        return None
    if not bcrypt.checkpw(password.encode(), user["password"].encode()):
        return None
    return UserInDb(**user)


async def get_user_by_email(email: str, db: firestore.client = Depends()) -> dict:
    users_ref = db.collection("users")
    query = users_ref.where("email", "==", email)
    docs = query.stream()
    for doc in docs:
        return doc.to_dict()
    return None


security = HTTPBearer()


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(security),
    db: firestore.client = Depends(),
) -> UserInDb:
    if token.scheme != "Bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme",
        )
    if not token.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token"
        )
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        user_doc = db.collection("users").document(user_id)
        user = user_doc.get()

        if not user.exists:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )
        return UserInDb(**user.to_dict())
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


async def require_authentication(
    current_user: UserInDb = Depends(get_current_user),
) -> UserInDb:
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    return current_user
