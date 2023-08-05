from copy import deepcopy
from secrets import token_urlsafe

class dictToClass:
    def __init__(self, variable_dict):
        for a, b in variable_dict.items():
            setattr(self, a, b)

class userDataToClass:
    def __init__(self, d: dict):
        self.variables = dictToClass(d.get("variables"))
        self.key = d.get("key")
        self.input = d.get("input")
        self.address = d.get("address")

class Users:
    def __adduser__(self, user: str, variableTemplate: dict, returnAddress: str):
        if not user in self.__getallusers__().keys():
            setattr(self, user, deepcopy(userDataToClass({"key": token_urlsafe(32), "variables": variableTemplate, "input": {}, "address": returnAddress})))
            
    def __removeuser__(self, user: str):
        if user in self.__getallusers__().keys():
            del self.__getallusers__()[user]

    def __getuser__(self, user: str):
        if user in self.__getallusers__().keys():
            return self.__getallusers__()[user]

    def __getallusers__(self):
        return {a: getattr(self, a) for a in dir(self) if not a.startswith('__')}

    def __init__(self):
        pass