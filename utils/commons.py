from pydantic import BaseModel
from utils.smallfuncs import *

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

class Item(BaseModel):
    name: str
    description: str | None = None
    value:  str | None = None
    

def get_user(db, username: str):
        if username in db:
            user_dict = db[username]
            return UserInDB(**user_dict)
        
with open(get_confparam("USER_LOCALDB_PATH")) as f:
    local_users_db = json.load(f)
