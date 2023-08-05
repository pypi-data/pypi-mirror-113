from pyxel import btnp as pyxel_btnp
from pyxel import btnr as pyxel_btnr
from flask import request as flask_request
from threading import Thread
from json import loads as json_loads
from pyxel_server.connection import webhost, webrequest
import pyxel_server.pyxelobj as pyxelobj

class run:
    def web(self, app):
        @app.route("/object", methods=["POST"])
        def object():
            incoming = json_loads(flask_request.data)
            if self.key == incoming.get("key"):
                obj = pyxelobj.obj(incoming.get("obj"))
                self.objects[obj.name] = obj
            return '', 204

        @app.route("/return/<return_key>", methods=["POST"])
        def data_return(return_key):
            incoming = json_loads(flask_request.data)
            if return_key in self.request.return_data.keys():
                self.request.return_data[return_key] = incoming
            return '', 204

    def __init__(self, ServerHost: str, ServerPort: str, ServerHTTPS: bool, ClientHost: str,ClientPort: str):
        self.port = ClientPort
        self.host = ClientHost
        if ServerHTTPS:
            self.server = "https://" + ServerHost + ":" + ServerPort
        else:
            self.server = "http://" + ServerHost + ":" + ServerPort
        self.return_data = {}
        self.objects = {}
        self.request = webrequest(self.host, self.port, self.server)
        self.webhostProcess = webhost(Host=self.host, Port=self.port, Web=self.web)
    
    def connect(self, User):
        index = 0
        self.user = str(User)
        while True:
            index += 1
            data = self.request.post("/init/" + self.user, json={})
            try:
                self.key = str(data["key"])
                break
            except:
                self.user = str(User) + str(index)

    def disconnect(self):
        data = self.request.post("/deinit/" + self.user, json={"key": self.key})
        if data["status"] == True:
            self.key = None
        else:
            print(data["status"])

    def getLocalVar(self, Variable, **Options):
        if Options.get("Value") == None:
            data = self.request.post("/var/local/" + self.user, json={"name": str(Variable), "key": self.key})
        else:
            data = self.request.post("/var/local/" + self.user, json={"name": str(Variable), "data": Options.get("Value"), "key": self.key})
        if data["status"] == True:
            return data["data"]
        else:
            print(data["status"])

    def getGlobalVar(self, Variable, **Options):
        if Options.get("Value") == None:
            data = self.request.post("/var/global/" + self.user, json={"name": str(Variable), "key": self.key})
        else:
            data = self.request.post("/var/global/" + self.user, json={"name": str(Variable), "data": Options.get("Value"), "key": self.key})
        if data["status"] == True:
            return data["data"]
        else:
            print(data["status"])

    def appinfo(self):
        data = self.request.post("/appinfo", json={})
        self.width = data.get("width")
        self.height = data.get("height")
        self.fps = data.get("fps")
        return data

    def btnp(self, button:int):
        if pyxel_btnp(button):
            Thread(target=self.request.post, args=("/input/" + self.user, {"name": str(button), "data": True, "key": self.key})).start()
            return True
        else:
            return False

    def btnr(self, button:int):
        if pyxel_btnr(button):
            Thread(target=self.request.post, args=("/input/" + self.user, {"name": str(button), "data": False, "key": self.key})).start()
            return True
        else:
            return False
    
    def predict(self, obj:pyxelobj.obj):
        obj.x += obj.addX
        obj.y += obj.addY
        return obj

    def addObject(self, obj:pyxelobj.obj):
        self.objects[obj.name] = obj

    def removeObject(self, objname:str):
        if objname in self.objects.keys():
            self.objects.pop(objname)

    def renderAll(self):
        for object in self.objects.keys():
            pyxelobj.render(self.objects[object])