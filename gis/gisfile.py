from utils.smallfuncs import *
from pydantic import BaseModel, Field

class GisFile():
    file_path = None
    col_key = None
    col_default_value = None
    dataset = None
    version= None

    def log_data(self, maxrows = 1000, col=None):
        if self.dataset is None: 
            info("Dataset is empty.")
            return
        info("=== DATASET PROPERTIES =========================================")
        info(f"Eikonic class : {self.__class__.__name__}")
        info(f"Data length : {len(self.dataset)}")
        info(f"Data source : {self.file_path}")
        info(f"Data contents is type : {type(self.dataset)}")
        info(f"Data key column is : {self.col_key}")
        info(f"Data default value column is : {self.col_default_value}")
        if hasattr(self, 'version'): info(f"Reference version : {self.version}")
        i_row = 1
        for index, row in self.dataset.iterrows():
            info("=== NEW ROW ====================================================")
            if self.col_key in row and self.col_key is None : 
                info(f"---- Index : {index}")
            else:
                info(f"---- Index : {index} | key : {row[self.col_key]}")
            if col is None or col not in row  : 
                info(row)
            else:
                info(f"---- {col} : {row[col]}")
            if i_row >= maxrows: 
                info(f"=== [Info] Interrupting display :\n(too many rows regarding maxrows parameters)\n.\n.\n.\n> shown {i_row} on {len(self.dataset)}")
                break
            i_row += 1
        info("================================================================")
    
    def show_data(self, maxrows = 1000, col=None):
        if self.dataset is None: 
            print("Dataset is empty.")
            return
        print("=== DATASET PROPERTIES =========================================")
        print(f"Eikonic class : {self.__class__.__name__}")
        print(f"Data length : {len(self.dataset)}")
        print(f"Data source : {self.file_path}")
        print(f"Data contents is type : {type(self.dataset)}")
        print(f"Data key column is : {self.col_key}")
        print(f"Data default value column is : {self.col_default_value}")
        if self.version is not None: print(f"Reference version : {self.version}")
        i_row = 1
        for index, row in self.dataset.iterrows():
            print("=== NEW ROW ====================================================")
            if self.col_key in row and self.col_key is None : 
                print(f"---- Index : {index}")
            else:
                print(f"---- Index : {index} | key : {row[self.col_key]}")
            if col is None or col not in row  : 
                print(row)
            else:
                print(f"---- {col} : {row[col]}")
            if i_row >= maxrows: 
                print(f"=== [print] Interrupting display :\n(too many rows regarding maxrows parameters)\n.\n.\n.\n> shown {i_row} on {len(self.dataset)}")
                break
            i_row += 1
        print("================================================================")
    
    def test_it(self, maxrows = 1000, col=None):
        self.show_data(maxrows, col)
        return {"is": "a", "correct": "return"}

    # For now : only encountered error, such as brackets
    def clean_col(self, col_to_clean, tokens_to_avoid = ["['","']"]):
        for ttk in tokens_to_avoid :
            self.dataset[col_to_clean] = self.dataset[col_to_clean].str.replace(ttk,'')
    
    def clean_key(self, tokens_to_avoid = None):
        if tokens_to_avoid is not None : self.clean_col(self.col_key,tokens_to_avoid)
        else : self.clean_col(self.col_key)
    
    def ao_getdataset(self):
        elts = self.dataset[[self.col_key, self.col_default_value,"geometry"]].to_geo_dict()
        toRet = []
        for eltf in elts['features']: 
            toRet.append(ao_GisFile(
                key=eltf['properties'][self.col_key], 
                dfv=eltf['properties'][self.col_default_value], 
                version = self.version if hasattr(self, 'version') else None,
                geom=eltf['geometry'])
                )
        return(toRet)

    def raw_getdataset(self, limit = None):
        if limit is not None: 
            toRet = self.dataset[[self.col_key, self.col_default_value,"geometry"]].head(limit).to_geo_dict()
        else:
            toRet = self.dataset[[self.col_key, self.col_default_value,"geometry"]].to_geo_dict()
        return(df_2_json(toRet,False))
    

class ao_GisFile(BaseModel):  
            key: str = Field()
            dfv: object = Field()
            version: object = Field(default="0.1")
            geom: object = Field()
        