from requests import request

from typing import Dict,Any

import json

class RestAPI:

    dir_       : str = ""
    function_  : str
    dictionary : Dict

    def __init__(self,paper : Dict) -> None:
        self.dictionary = paper

    def check_dir(self, dir_ : str):
        return dir_ in [_ for _ in self.dictionary]

    def check_function(self,function_ : str):
        return function_ in [_ for _ in self.dictionary[self.dir_]]
    
    def check_agrs(self, check : Any,args : Dict):
        if check != {}:
            return len([_ for _ in args if _ not in [__ for __ in check]]) == 0
        return True
    
    @property
    def sub_dir(self) -> str:
        return self.fuction_
    
    @sub_dir.setter
    def sub_dir(self,value : str) -> None:
        if self.check_function(value):
            self.function_ = value

    @property
    def path(self) -> str:
        return self.dir_
    
    @path.setter
    def path(self,value : str) -> None:
        if self.check_dir(value):
            self.dir_ = value

    def exec(self,args : Dict) -> Dict:
        if self.check_dir(self.dir_):
            if self.check_function(self.function_):
                data = self.dictionary[self.dir_][self.function_]
                if "json" in [_ for _ in data]:
                    if not self.check_agrs(data["json"],args):
                        raise "Invalid args\n Rules: {}".format(data["json"])
                    data["json"] = args
                if "parms" in [_ for _ in data]:
                    if not self.check_agrs(data["parms"],args):
                        raise "Invalid args\n Rules: {}".format(data["json"])
                    data["parms"] = args
                data["url"] = self.dictionary["end_point"]+self.dir_
                output = request(**data)
                try:
                    return output.json()
                except:
                    return output.text()
            else:
                raise "Invalid Function"
        else:
            raise "Invalid Dir"