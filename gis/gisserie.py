from gis.shpfile import ShpFile

class GisSerie(ShpFile):
    def __init__(self, file_path, col_key, col_default_value = None, keyexpression = None, valueexpression = None):
        super().__init__(file_path, col_key, col_default_value, keyexpression, valueexpression)
 