from efastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from gis.gisserie import GisSerie
import uvicorn


class EikoFastApi():
    def __init__(self):
        self.app = FastAPI()
        @self.app.get("/")
        async def root():
            return {"message": "Hello World"}
        @self.app.get("/GisSerie/")
        async def gis_serie(filepath, key, dfvalue, key_expression , value_expression):
            gs = GisSerie(filepath, key, dfvalue, key_expression , value_expression)
            return JSONResponse(content=jsonable_encoder(gs.getinfos()), media_type='application/json')

    def run(self, apiport=8000, apihost="0.0.0.0"):
       uvicorn.run(self.app, apihost, apiport)

