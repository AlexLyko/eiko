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

def oauthgithub_set(app,oauth2_scheme):   
    GITHUB_CLIENT_ID = get_confparam("GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET = get_confparam("GITHUB_CLIENT_SECRET")
    APP_BASEURL = get_confbaseurl()
    SECRET_KEY = get_confparam("SECRET_KEY")
    ALGORITHM = get_confparam("ALGORITHM")

    oauth2_scheme = OAuth2AuthorizationCodeBearer(
        authorizationUrl=f'{APP_BASEURL}/github-authorize',
        tokenUrl=f'{APP_BASEURL}/token',
    )

    @app.get("/github-authorize")
    async def github_authorize(request: Request):
        redirect_uri = request.query_params.get("redirect_uri")
        state = request.query_params.get("state")

        params = {
            "client_id": GITHUB_CLIENT_ID,
            "redirect_uri": redirect_uri,
            "scope": "read:user user:email",
            "state": state
        }
        url = f'https://github.com/login/oauth/authorize?{urllib.parse.urlencode(params)}'
        return RedirectResponse(url, status_code=303)

    @app.post("/token")
    async def exchange_token(code: str = Form(...), redirect_uri: str = Form(...)):
        async with httpx.AsyncClient() as client:
            github_response = await client.post(
                "https://github.com/login/oauth/access_token",
                headers={"Accept": "application/json"},
                data={
                    "client_id": GITHUB_CLIENT_ID,
                    "client_secret": GITHUB_CLIENT_SECRET,
                    "code": code,
                    "redirect_uri": redirect_uri,
                },
            )
            json_resp = github_response.json()

            if "error" in json_resp:
                raise HTTPException(status_code=400, detail=json_resp.get("error_description", "OAuth error"))
            github_token = json_resp.get("access_token")

            if not github_token:
                raise HTTPException(status_code=400, detail="GitHub token exchange failed")
        
            # Fetch user data from GitHub
            user_resp = await client.get(
                "https://api.github.com/user",
                headers={"Authorization": f"token {github_token}"}
            )
            user_data = user_resp.json()
            github_id = user_data.get("id")

            # Generate JWT token for the app
            return create_access_token({
                "sub": str(github_id),
                "email": user_data.get("email") or "unknown@example.com",
                "full name" : user_data.get("name"),
                "id" : user_data.get("id"),
                "username" : user_data.get("login")
            })

         
    
    @app.get("/docs", include_in_schema=False)
    async def overridden_swagger():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title="Eiko",
            oauth2_redirect_url=f'{APP_BASEURL}/docs/oauth2-redirect',
            init_oauth={
                "clientId": GITHUB_CLIENT_ID,
                "usePkceWithAuthorizationCodeGrant": False,
            },
        )
    
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
    return oauth2_scheme

