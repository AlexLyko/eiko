
from jose import JWTError
import jwt
from utils.oauth_jwt import create_access_token
import urllib.parse
from fastapi import Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.openapi.docs import get_swagger_ui_html
import httpx
from utils.smallfuncs import *
from utils.commons import *

from fastapi import HTTPException, Depends, status
from typing import Annotated

"""
This code is NOT WORKING, but I found really convincing approaches and choose to write it down.
I don't have a KeyCloak available service right now, and I will finalize it later.
I give a try to @benjaminbuffet proposal here.
"""

def oauthkeycloak_set(app,oauth2_scheme):   
    # APP_BASEURL = get_confbaseurl()
    KEYCLOAK_TOKEN_URL = get_confparam("KEYCLOAK_TOKEN_URL") # I'll bet on http://127.0.0.1/token if @benjaminbuffet proposal is not working, code : f'{APP_BASEURL}/token'. It works as a callback for github, hope to keep it here.
    KEYCLOAK_OAUTH_URL = get_confparam("KEYCLOAK_OAUTH_URL")
    KEYCLOAK_TOKEN_RURL = get_confparam("KEYCLOAK_TOKEN_RURL") # I'll bet on http://127.0.0.1/token if @benjaminbuffet proposal is not working, code : f'{APP_BASEURL}/token'. It works as a callback for github, hope to keep it here.
    KEYCLOAK_CLIENT_ID = get_confparam("KEYCLOAK_CLIENT_ID")
    KEYCLOAK_CLIENT_SECRET = get_confparam("KEYCLOAK_CLIENT_SECRET")
    SECRET_KEY = get_confparam("SECRET_KEY")
    ALGORITHM = get_confparam("ALGORITHM")  

    oauth2_scheme = OAuth2AuthorizationCodeBearer(
            tokenUrl=KEYCLOAK_TOKEN_URL,
            authorizationUrl=KEYCLOAK_OAUTH_URL,
            refreshUrl=KEYCLOAK_TOKEN_RURL,
    )

    # @app.post("/token") 
    async def exchange_token(code: str = Form(...), redirect_uri: str = Form(...)):
        ## I didn't test this part. Really not sure.
        async with httpx.AsyncClient() as client:
            try :
                user = kc_get_data("try")
                return create_access_token({
                            "sub": user.username,
                            "email": user.email,
                            "full name" : user.full_name,
                            "id" : user.username,
                            "username" : user.username
                })
            except:
                ## Other way is to mimic what's done for other OAuth modes :            
                keycloak_response = await client.post(
                    KEYCLOAK_TOKEN_URL,
                    headers={"Accept": "application/json"},
                    data={
                        "client_id": KEYCLOAK_CLIENT_ID,
                        "client_secret": KEYCLOAK_CLIENT_SECRET,
                        "code": code,
                        "redirect_uri": redirect_uri,
                    },
                )
                json_resp = keycloak_response.json()

                if "error" in json_resp:
                    raise HTTPException(status_code=400, detail=json_resp.get("error_description", "OAuth error"))
                keycloak_token = json_resp.get("access_token")

                if not keycloak_token:
                    raise HTTPException(status_code=400, detail="keycloak token exchange failed")
                
                ## This part retrieve data from KeyCloak server, needs to be dev
                ## I don't ever think Keycloak is a proper storage tool
                #### First try : as done with Github 
                try:
                    user_resp = await client.get("https://api.keycloak.com/user", headers={"Authorization": f"token {keycloak_token}"})
                    user_data = user_resp.json()
                except:
                ### If it fails, run with the login in fake_db
                #### Second try : as done with Fake local Db 
                    user = get_user(local_users_db, keycloak_token.id) #We hope we can find a match
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
    async def get_me(token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid JWT")
        
        return {
            "user_id": payload.get("sub"),
            "email": payload.get("email")
        }
    
    # This code is not mine.
    # See at https://medium.com/@benjaminbuffet/s%C3%A9curiser-fastapi-avec-keycloak-partie-2-2e31f14a225d
    # Given example says it manages to deal everything with this kind of functions.
    # Guess I can have scope value errors, considering oauth2_scheme and the fact that we already are in a function.
    # This solution considers that OAuth2AuthorizationCodeBearer is fully compatible with KeyCloak, and that we can already use the token.
    async def kc_valid_access_token(access_token: Annotated[str, Depends(oauth2_scheme)]):
            optional_custom_headers = {"User-agent": "custom-user-agent"}
            jwks_client = jwt.PyJWKClient(get_confparam("KEYCLOAK_CERTS_URL"), headers=optional_custom_headers)
            try:
                signing_key = jwks_client.get_signing_key_from_jwt(access_token)
                data = jwt.decode(
                    access_token,
                    signing_key.key,
                    algorithms=["RS256"],
                    audience="api",
                    options={"verify_exp": True},
                )
                return data
            except jwt.exceptions.InvalidTokenError:
                raise HTTPException(status_code=401, detail="Not authenticated")


    async def kc_get_data(token_data: Annotated[dict, Depends(kc_valid_access_token)]):
            return token_data["resource_access"]["api"]
    
    return oauth2_scheme




