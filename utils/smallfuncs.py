import logging
import random, string
import zipfile, os, aiofiles
import shutil
from fastapi import Response
import json
from dotenv import load_dotenv
from passlib.context import CryptContext
from pathlib import Path


load_dotenv()

def get_confparam(id_param, format:str = "str"):
    match(format):
        case "int": return int(os.getenv(id_param))            
    return os.getenv(id_param)


logger = logging.getLogger(__name__)
logIsSet = False
crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_crypt_context():
    return crypt_context



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
    ensure_foutput(outputfolder)
    with zipfile.ZipFile(input_file, 'r') as zip_ref:
        zip_ref.extractall(outputfolder)

def zip(input_src, out_file_path):
    ensure_foutput(out_file_path, True)
    if os.path.isfile(input_src): 
        zip = zipfile.ZipFile(out_file_path, "w", zipfile.ZIP_DEFLATED)
        zip.write(input_src)
        zip.close()
    elif(os.path.isdir(input_src)): 
        print(out_file_path)
        shutil.make_archive(out_file_path, 'zip', input_src) # Better than zipfile, cause using recursive becomes hacky when the output zip is located in the output folder.
        
async def upload_file(file):
    out_file_path= f'{str(get_confparam("FILE_UPLOAD_PATH"))}/{random_str()}/{file.filename}'
    ensure_foutput(out_file_path)
    async with aiofiles.open(out_file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content) 
        await out_file.close() 
    return out_file_path

def df_2_json(df, validated=True):
    if validated : return Response(df.to_json(), media_type="application/json")
    else : return json.dumps(df)

def as_write_in_file(outputfile_path, file_contents):
    ensure_foutput(outputfile_path)
    with open(outputfile_path, "w") as outputfile:
        outputfile.write(file_contents)
        outputfile.close()

def ensure_foutput(outputfile_path, isFile = None):
    # For now, I won't try a pathvalidate cause I don't wanna multiple the packages. I'll just check that the last chunk after the last "/" contains "." (barely, that the file ends with and extension)
    #path = Path(outputfile_path).parent if os.path.isfile(outputfile_path) else Path(outputfile_path) #File or dir not created yet !
    path= None
    if isFile is None:
        path = Path(outputfile_path).parent if "." in outputfile_path.split("/|\\")[-1] else outputfile_path
    elif isFile : 
        path = Path(outputfile_path).parent
    elif not isFile :
        path = Path(outputfile_path).parent
    os.makedirs(path, exist_ok=True)