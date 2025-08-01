import logging
import random, string
import zipfile, os, aiofiles
from fastapi import Response
import json
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()

logger = logging.getLogger(__name__)
logIsSet = False
crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_crypt_context():
    return crypt_context

def get_confparam(id_param, format:str = "str"):
    match(format):
        case "int": return int(os.getenv(id_param))            
    return os.getenv(id_param)

def get_confbaseurl():
    return f'{get_confparam("APP_PROTOCOL")}{get_confparam("APP_DNS")}:{ get_confparam("APP_PORT")}'

def con_log():
    logging.basicConfig(filename='./logs/eiko.log',
                        level=logging.INFO,
                        format= '[%(asctime)s] %(levelname)s - %(message)s',
                        datefmt='%H:%M:%S')
    logIsSet = True

def info(whattolog):
    if not logIsSet: con_log()
    logger.info(whattolog)

def random_str(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unzip(input_file, outputfolder):
    os.makedirs(outputfolder)
    with zipfile.ZipFile(input_file, 'r') as zip_ref:
        zip_ref.extractall(outputfolder)

async def upload_file(file):
    out_upload_path = "/".join(["uploaded/",random_str()])
    os.makedirs(out_upload_path)
    out_file_path = "/".join([out_upload_path,file.filename])
    async with aiofiles.open(out_file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content) 
    return out_file_path

def df_2_json(df, validated=True):
    if validated : return Response(df.to_json(), media_type="application/json")
    else : return json.dumps(df)