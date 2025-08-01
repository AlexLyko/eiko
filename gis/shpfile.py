import geopandas as gpd
import pandas as pd
from gis.gisfile import GisFile

class ShpFile(GisFile):
    def __init__(self, file_path, col_key, col_default_value = None, keyexpression = None, valueexpression = None):
        self.file_path = file_path
        self.col_key = col_key
        self.col_default_value = col_default_value
        self.keyexpression = keyexpression
        self.valueexpression = valueexpression
        self.dataset = gpd.read_file(self.file_path)
        if self.keyexpression is not None : self.eval_column(self.col_key, self.rewrite_evalexpr(self.keyexpression))
        if self.valueexpression is not None : self.eval_column(self.col_default_value, self.rewrite_evalexpr(self.valueexpression))
        self.clean_key()

    def eval_column(self, target_col, eval_expr):     
        d=self.dataset
        self.dataset = pd.eval(f"{target_col} = {eval_expr}", target=self.dataset)

    # For now : only "+" for string objects
    def rewrite_evalexpr(self, expression):
        concat = []
        splits = expression.split("+")
        for sp in splits:
            if sp in self.dataset:
                if self.dataset.dtypes[sp] == "object": concat.append(f"d.{sp}.astype('string')")
                else: concat.append(f"d.{sp}")
            else: concat.append(sp)
        return "+".join(concat)
    





"""
from shapely.geometry import shape as shapely

def read_shp(package="fiona", shp_path="./tests/datasets/series/IlleEtVilaine_Simplified.shp"):

    match package:
        case "fiona":
            import fiona
            first = None
            with fiona.open(shp_path) as shapes:
                for record in shapes:
                    if first is None: first = record 
                    print(record)
            shp_geom = shapely(first['geometry']) 

        case "pyshp":
            import shapefile
            shape = shapefile.Reader(shp_path)
            #first feature of the shapefile
            feature = shape.shapeRecords()[0]
            first = feature.shape.__geo_interface__  
            print(first) # (GeoJSON format)
            shp_geom = shapely(first)


        case "geopandas":
            import geopandas as gpd
            shapefile = gpd.read_file(shp_path)
            print(shapefile)
            shp_geom=shapefile.loc[0, 'geometry']


    print(shp_geom)
    print(type(shp_geom))
"""