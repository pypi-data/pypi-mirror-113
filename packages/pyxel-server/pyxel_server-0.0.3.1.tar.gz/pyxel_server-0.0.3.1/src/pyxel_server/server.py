# Import modules
from json import loads as json_loads
from flask import request
from time import sleep
from pyxel_server import data
from pyxel_server import connection
from pyxel_server import pyxelobj
from requests import post as requests_post
class run:
    def web(self, app):
        @app.route("/appinfo", methods=["POST"])
        def get_info():
            incoming = json_loads(request.data)
            # send basic data to client 
            self.webhost.send({
                "width": self.AppWidth,
                "height": self.AppHeight,
                "fps": self.AppFPS
            }, incoming.get("return-address"))
            return '', 204
        @app.route("/init/<user>", methods=["POST"])
        def init_user(user: str):
            incoming = json_loads(request.data)
            print(incoming)
            # Checks if user exists
            if not hasattr(self.Users, user):
                try:
                    # if there is max client variable it will check if there are too many clients
                    if not len(vars(self.Users)) == self.maxClients:
                        # create client
                        self.Users.__adduser__(user, self.localVariablesTemplate, incoming.get("return-address"))
                        self.webhost.send({
                            "key": self.Users.__getuser__(user).key,
                            "status": True
                        }, incoming.get("return-address"))
                except:
                    # client client
                    self.Users.__adduser__(user, self.localVariablesTemplate, incoming.get("return-address"))
                    self.webhost.send({
                        "key": self.Users.__getuser__(user).key,
                        "status": True
                    }, incoming.get("return-address"))
            else:
                # If exists return error
                self.webhost.send({
                    "status": "USER_TAKEN"
                }, incoming.get("return-address"))
            return '', 204
        @app.route("/deinit/<user>", methods=["POST"])
        def deinit_user(user: str):
            # saves all post data into variable
            incoming = json_loads(request.data)
            # if user exists
            Client = self.Users.__getuser__(user)
            if not Client == None:
                # if key matches server saved key
                if Client.key == incoming.get("key"):
                    # remove user
                    self.Users.__removeuser__(user)
                    # return success
                    self.webhost.send({
                        "status": True
                    }, incoming.get("return-address"))
                else:
                    #if not, return error
                    self.webhost.send({
                        "status": "KEY_INVALID"
                    }, incoming.get("return-address"))
            else:
                #if does not exist, return error
                self.webhost.send({
                    "status": "USER_INVALID"
                }, incoming.get("return-address"))
            return '', 204
        @app.route("/var/global/<user>", methods=["POST"])
        def get_global_variable(user: str):
            # saves all post data into variable
            incoming = json_loads(request.data)
            # if user exists
            Client = self.Users.__getuser__(user)
            if not Client == None:
                # if key matches server saved key
                if Client.key == incoming.get("key"):
                    name = str(incoming.get("name"))
                    data = incoming.get("data")
                    # if value is not none
                    if not data == None:
                        # change global variable to value
                        self.variables[name] = data
                    # sends success and value of the global variable
                    self.webhost.send({
                        "data": self.variables[name],
                        "status": True
                    }, incoming.get("return-address"))
                else:
                    #if not, return error
                    self.webhost.send({
                        "status": "KEY_INVALID"
                    }, incoming.get("return-address"))
            else:
                #if does not exist, return error
                self.webhost.send({
                    "status": "USER_INVALID"
                }, incoming.get("return-address"))
            return '', 204
        @app.route("/var/local/<user>", methods=["POST"])
        def get_local_variable(user: str):
            # saves all post data into variable
            incoming = json_loads(request.data)
            # if user exists
            Client = self.Users.__getuser__(user)
            if not Client == None:
                # if key matches server saved key
                if Client.key == incoming.get("key"):
                    name = str(incoming.get("name"))
                    data = incoming.get("data")
                    variable = getattr(Client.variables, name)
                    # if value is not none
                    if not data == None:
                        # change local variable to value
                        variable = data
                    # sends success and value of the global variable
                    self.webhost.send({
                        "data": variable,
                        "status": True
                    }, incoming.get("return-address"))
                else:
                    #if not, return error
                    self.webhost.send({
                        "status": "KEY_INVALID"
                    }, incoming.get("return-address"))
            else:
                #if does not exist, return error
                self.webhost.send({
                    "status": "USER_INVALID"
                }, incoming.get("return-address"))
            return '', 204
        @app.route("/input/<user>", methods=["POST"])
        def update_input(user):
            # saves all post data into variable
            incoming = json_loads(request.data)
            # if user exists
            Client = self.Users.__getuser__(user)
            if not Client == None:
                # if key matches server saved key
                if Client.key == incoming.get("key"):
                    name = str(incoming.get("name"))
                    data = bool(incoming.get("data"))
                    # if value is true
                    if not data == None:
                        # add key pressed
                        Client.input[name] = data
            
                    self.webhost.send({
                        "status": True
                    }, incoming.get("return-address"))
                else:
                    #if not, return error
                    self.webhost.send({
                        "status": "KEY_INVALID"
                    }, incoming.get("return-address"))
            else:
                #if does not exist, return error
                self.webhost.send({
                    "status": "USER_INVALID"
                }, incoming.get("return-address"))
            return '', 204

        try:
            self.webScript(self, app)
        except:
            pass

    def __init__(self, Host, Port, AppWidth, AppHeight, AppFPS, UpdateScript, **others):
        # Set host and port
        self.host = str(Host)
        self.port = str(Port)
        # Set update script to run when update() is called
        self.updateScript = UpdateScript
        # Set default app fps
        self.AppWidth = int(AppWidth)
        self.AppHeight = int(AppHeight)
        self.AppFPS = int(AppFPS)
        # Set web script if there is
        if not others.get("WebScript") == None:
            self.webScript = others.get("WebScript")
        # Set init script if there is
        if not others.get("InitScript") == None:
            self.initScript = others.get("InitScript")
        # Set max clients available to connect
        if not others.get("MaxClients") == None:
            self.maxClients = int(others.get("MaxClients"))
        # Set global variables
        if not others.get("GlobalVariables") == None:
            self.variables = data.dictToClass(others.get("GlobalVariables"))
        # Creates local variable template
        self.localVariablesTemplate = {}
        if not others.get("LocalVariables") == None:
            self.localVariablesTemplate = others.get("LocalVariables")
        
        # Define other variables
        self.frame_count = 0 
        self.Users = data.Users()
        self.running = True
        # If init script is set
        try:
            # Runs script
            self.initScript(self)
        except:
            pass

        self.run()

    def sendObj(self, obj:pyxelobj.obj):
        jsonobj = pyxelobj.new(obj.name, obj.x, obj.y, obj.addX, obj.addY, obj.image)
        for Username, User in self.Users.__getallusers__().items():
            try:
                requests_post(User.address + "/object", json={"obj": jsonobj, "key": User.key})
            except:
                pass
    #main loop
    def run(self):
        self.webhost = connection.webhost(Host=self.host, Port=self.port, Web=self.web)
        #will stop if running is false
        while self.running:
            # run update function
            self.updateScript(self)
            # Add 1 to frame count
            self.frame_count += 1
            # waits
            sleep(1 / self.AppFPS)