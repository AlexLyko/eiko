
from fastapi import Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from jwt import InvalidTokenError
from utils.smallfuncs import *
from utils.commons import *


SECRET_KEY = get_confparam("SECRET_KEY")
ALGORITHM = get_confparam("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = get_confparam("ACCESS_TOKEN_EXPIRE_MINUTES", "int")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None)-> Token:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return Token(access_token=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM), token_type="bearer")

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def configure_app(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:8000",
            "http://127.0.0.1:8000",
             get_confbaseurl()
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
