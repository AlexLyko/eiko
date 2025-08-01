
from fastapi import HTTPException, Depends, status
from typing import Annotated

from jose import JWTError
from utils.smallfuncs import *
from utils.commons import *
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from utils.oauth_jwt import create_access_token



def oauthlocal_set(app, oauth2_scheme):
    SECRET_KEY = get_confparam("SECRET_KEY")
    ALGORITHM = get_confparam("ALGORITHM")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    crypt_context = get_crypt_context()

    @app.post("/token")
    async def exchange_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
                user = oauthlocal_authenticate_user(local_users_db, form_data.username, form_data.password)
                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Incorrect username or password",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                return create_access_token({
                    "sub": user.username,
                    "email": user.email,
                    "full name" : user.full_name,
                    "id" : user.username,
                    "username" : user.username
                })
                
    
    @app.get("/me")
    async def get_me(token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except InvalidTokenError:
            raise credentials_exception
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid JWT")
        user = get_user(local_users_db, username=token_data.username)
        if user is None:
            raise credentials_exception
        return user
    
    def oauthlocal_verify_password(plain_password, hashed_password):
            return crypt_context.verify(plain_password, hashed_password)

    def oauthlocal_authenticate_user(fake_db, username: str, password: str):
            user = get_user(fake_db, username)
            if not user:
                return False
            if not oauthlocal_verify_password(password, user.hashed_password):
                return False
            return user      
    return oauth2_scheme






