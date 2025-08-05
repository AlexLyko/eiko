import uvicorn
from fastapi import Depends, FastAPI, UploadFile, Query
from fastapi_pagination import Page, add_pagination, paginate
from fastapi.responses import PlainTextResponse
from typing import Optional
from typing import Optional
from gis.gisserie import GisSerie
from gis.reference import Reference
from gis.gisfile import ao_GisFile

from utils.smallfuncs import *
from utils.commons import *
from utils.oauth_github import *
from utils.oauth_local import *  
from utils.oauth_jwt import *
#from utils.oauth_keycloak import *
from utils.parsedclass import ParsedScenario


OAUTH_MODE = get_confparam("OAUTH_MODE")

oauth2_scheme = None
app = FastAPI()
add_pagination(app)
configure_app(app)

# OAuth is not set to work with classes... routes and dependencies soon become messy. Quite a hack here !
# oauth_2_scheme (local to each script, but resulting with a strong impact on FastAPI) and get_current_user are dynamically set by this import.
# I'd like to use classes, but Python is not Java.
match(OAUTH_MODE):
    case "local_db" :       
        oauth2_scheme = oauthlocal_set(app, oauth2_scheme)
    case "github" :
        oauth2_scheme = oauthgithub_set(app, oauth2_scheme)
    case "keycloak": # not done yet
       # oauthkeycloak_set(app)
       pass

@app.get("/")
async def root():
    return {"message": "εiko is an interface for knowledge operations"}

async def valid_access_token(token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            print(payload)
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid JWT")
        return {
            "user_id": payload.get("sub"),
            "email": payload.get("email")
        }

@app.post("/GeneratePwd/", dependencies=[Depends(valid_access_token)])
async def generate_pwd(expression_to_encode: str = "secret"):
    crypt_context = get_crypt_context()
    return Item(
        name= "encoded_expression",
        description= "using production crypto context of Eiko",
        value= crypt_context.hash(expression_to_encode)
    )

@app.post("/Scenario/", dependencies=[Depends(valid_access_token)])
async def scenario(jsonfile: UploadFile):
    out_file_path = await upload_file(jsonfile)
    ps= ParsedScenario(out_file_path)
    return Item(
        name="Scenario output",
        description="Output of the execution of the scenario",
        value= ps.export()
    )

@app.post("/GisSerie/", dependencies=[Depends(valid_access_token)])
async def gis_serie(file: UploadFile, key_expression, value_expression, key="key", dfvalue="dfv")-> Page[ao_GisFile]:
    out_file_path = await upload_file(file)
    gs = GisSerie(out_file_path, key, dfvalue, key_expression , value_expression)
    return paginate(gs.ao_getdataset())

@app.post("/raw/GisSerie/",response_class=PlainTextResponse)
async def gis_serie(file: UploadFile, key_expression, value_expression, limit: Optional[int] = Query(default=None, example="10"), key="key", dfvalue="dfv"):
    out_file_path = await upload_file(file)
    print(limit)
    gs = GisSerie(out_file_path, key, dfvalue, key_expression , value_expression)
    return gs.raw_getdataset(limit)

@app.post("/Reference/")
async def gis_serie(file: UploadFile, version="1.0", key="key", dfvalue="dfv", key_expression=None, value_expression=None, validated: bool=True)-> Page[ao_GisFile]:
    out_file_path = await upload_file(file)
    gs = Reference(out_file_path, version, key, dfvalue, key_expression , value_expression)
    return paginate(gs.ao_getdataset())

@app.post("/raw/Reference/",response_class=PlainTextResponse)
async def gis_serie(file: UploadFile, key="key", dfvalue="dfv", key_expression=None, value_expression=None, limit:int=10):
    out_file_path = await upload_file(file)
    gs = Reference(out_file_path, key, dfvalue, key_expression , value_expression)
    return gs.raw_getdataset(limit)


# You can add additional URLs to this list, for example, the frontend's production domain, or other frontends.

if __name__ == "__main__":
    uvicorn.run("efastapi:app", host="0.0.0.0", port=8000, reload=True)
