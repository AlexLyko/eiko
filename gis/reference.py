from gis.shpfile import ShpFile

class Reference(ShpFile):
    def __init__(self, file_path, version, col_key, col_default_value = None, keyexpression = None, valueexpression = None, version_format = None):
        super().__init__(file_path, col_key, col_default_value, keyexpression, valueexpression)
        self.version = version
        
