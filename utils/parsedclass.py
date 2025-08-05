
from utils.smallfuncs import *
import importlib
import json

class ParsedClass():
    iclass = None
    def __init__(self, classname: str, args):
        class_strs= classname.split(".")
        self.package_name = classname.lower() #class_strs[0] if len(class_strs)>1 else None
        self.class_name = class_strs[1] if len(class_strs)>1 else class_strs[0]
        self.package=  importlib.import_module(self.package_name) if self.package_name else None
        self.iclass = getattr(self.package, self.class_name)(**args)
    def func(self, func_name, args=None):
        if args :
            return getattr(self.iclass, func_name)(**args)
        else:
            return getattr(self.iclass, func_name)()

class ParsedStep():
    vars = {}
    json_data= {}
    object= None
    func_ret= None
    VERBOSE= False

    def __init__(self, json_data, vars, verbose= False):
        self.vars= vars
        self.json_data= json_data
        self.VERBOSE= verbose
    
    def exec(self):
        self.setClass()
        if "objectRef" in self.json_data: 
            if self.VERBOSE: print(f'Placed in reference : {self.json_data["objectRef"]}')
            self.vars[self.json_data["objectRef"]]= self.object
        self.execFunction()
        if "functionRef" in self.json_data: 
            if self.VERBOSE: print(f'Placed in reference : {self.json_data["functionRef"]}')
            self.vars[self.json_data["functionRef"]]= self.func_ret

    def setClass(self):
        if self.VERBOSE: print(f'Class {self.json_data["class"]}')
        if self.json_data["class"].startswith("#"):
            self.object= self.vars[self.json_data["class"]]
            return
        object_args= {}
        if "objectArgs" in self.json_data: 
            for key, value  in self.json_data["objectArgs"].items():
                object_args[key]= self.vars(value) if value.startswith("#") else value
        self.object= ParsedClass(self.json_data["class"], object_args)

    def execFunction(self):
        if "function" not in self.json_data: return
        if self.VERBOSE: print(f'Function {self.json_data["function"]}')
        func_args= {}
        if "functionArgs" not in self.json_data: return
        for key, value  in self.json_data["functionArgs"].items():
           func_args[key]= self.vars(value) if key.startswith("#") else value
        self.func_ret= self.object.func(self.json_data["function"], func_args)
    
    def get_vars(self): return self.vars

class ParsedScenario():
    json_data= None
    VERBOSE = False
    uniq_id = None

    def __init__(self, jsonpath="assets/test.json", exec= True):
        self.uniq_id= random_str(size= 12)
        with open(jsonpath) as f:
            self.json_data = json.load(f)
        if "verbose" in self.json_data["params"]: self.VERBOSE= True
        if exec: self.exec()
    
    def exec(self):
        vars= {}
        i = 1
        while i < 6:
            idx= str(i)    
            if self.VERBOSE :
                print(f'Step {idx}')
                print(f'Current variables : ')
                for key, value in vars.items(): print(f"{key}: {value}")
            if idx in self.json_data:
                ps = ParsedStep(self.json_data[idx], vars, self.VERBOSE)
                ps.exec()
                vars = ps.get_vars()  
            i += 1 
    def get_json(self): return self.json_data
    def export(self):
        return self.uniq_id # TODO: chose a strategy to implement for result downloading