# Pyxel Server
A simple to use API for integration between your [Pyxel](https://github.com/kitao/pyxel) games with servers.  
![preview](https://github.com/FloppiDisk/pyxel_server/raw/main/preview.gif?raw=true)
# Install
```
pip install pyxel-server
```  
or
```
https://pypi.org/project/pyxel-server/
```
# Example
## Code
### client.py
```python
import pyxel
from pyxel_server import client

class App:
    def __init__(self):
        self.address = input("Server Address: ")
        self.port = input("Server Port: ")
        self.clientPort = input("Client Port: ")
        self.username = input("Choose Username: ")
        self.Updating = False
        self.points = 0
        # Connects to server and runs pyxel app
        self.client = client.run(self.address, self.port, False, "127.0.0.1", self.clientPort)
        self.client.connect(self.username)
        self.client.appinfo()
        pyxel.init(self.client.width, self.client.height, caption=self.username, fps=self.client.fps, quit_key=pyxel.KEY_F2)
        pyxel.run(self.update, self.draw)
    def update(self):
        self.Updating = True
        # Custom Quit Key, Force quit is F2
        if pyxel.btnr(pyxel.KEY_ESCAPE):
            self.client.disconnect()
            pyxel.quit()
        # Checks if button is pressed and sends to server
        self.client.btnp(pyxel.KEY_SPACE)
        # Every half second it will get the user's points
        if pyxel.frame_count % round(pyxel.DEFAULT_FPS / 2) == 0:
            self.points = self.client.getLocalVar("points")
        self.Updating = False
    def draw(self):
        if not self.Updating:
            # Clear screen
            pyxel.cls(0)
            # Draw score
            pyxel.text(0, 0, str(self.points), 10)
            # Render all objects
            self.client.renderAll()
App()
```
### server.py
```python
from pyxel_server import pyxelobj, server
import pyxel
import random

def update(self):
    # If the dot is not activated
    if not self.variables.activated:
        # Create a new one and send it
        self.variables.x = random.randrange(0, 256)
        self.variables.y = random.randrange(0, 144)
        obj = pyxelobj.obj(pyxelobj.new("dot", self.variables.x, self.variables.y, 0, 0, [[7]]))
        self.variables.activated = True
        self.sendObj(obj)
    # Loops through every single user
    for Username, User in self.Users.__getallusers__().items():
        # If user pressed space
        if User.input.get(str(pyxel.KEY_SPACE)) and self.variables.visible:
            # Add 1 point to user
            User.variables.points += 1
            # Set the dot to be not activated
            self.variables.pressed = False
            User.input[str(pyxel.KEY_SPACE)] = False
            
LocalVariables = {
    "points": 0
}
GlobalVariables = {
    "pressed": False,
    "x": random.randrange(0, 256),
    "y": random.randrange(0, 144)
}
server.run("127.0.0.1", "5000", 256, 144, 12, update,LocalVariables=LocalVariables, GlobalVariables=GlobalVariables)
```
## What will happen
This is a game of who pressed space first when the dot apears.
## [More](https://github.com/FloppiDisk/pyxel_server/tree/main/examples)
# Contributing
## Issues and Suggestions
Submit the issue or suggestion using the issue tracker, make sure it has not been repeated.  
### Issues
It should include the os, error, python modules used, python version and other relevant information.  
### Suggestions
It should include sample usages, mock-ups and other relevant information.  
## Patches, Feature implementations, and Optimizations
Please submit it in a pull request, issues should be listed if it is a fix.  
  Note: All pull requests submitted are licensed under the [MIT License](https://github.com/FloppiDisk/pyxel_server/blob/main/LICENSE)  
# Reference
Note: `pyxel_server`'s intended features are not fully implemented yet.
## server
### System
* `run(Host, Port, AppWidth, AppHeight, AppFPS, UpdateScript, [WebScript], [InitScript], [Variables])`  
Initializes the server and runs it.  
`Host`: The ip or domain of the server. e.g. `Host="127.0.0.1"`  
`Port`: The port to be opened in the `Host`. e.g. `Port="5000"`  
`AppWidth`: The width of the client's window when connected. e.g. `AppWidth=256`  
`AppHeight`: The height of the client's window when connected. e.g. `AppHeight=144`  
`AppFPS`: The FPS of the client's window when connected. e.g. `AppFPS=24`  
`UpdateScript`: The function to run every 1/`AppFPS`. e.g. `UpdateScript=update`  
  Note: The function must have the parameter `self`.  
`WebScript`: The custom flask events and routes. e.g. `WebScript=web`  
  Note: The function must have the parameter `self` & `app`.  
`InitScript`: The custom initialization function that will be called when `server()` is called. e.g. `InitScript=init`  
  Note: The function must have the parameter `self`.  
`Variables`: A dictionary of variables needed. e.g. `Variables={"Name": "Value"}`  
### Connection
* `sendObj(obj)`  
Converts obj to a json format and sends to all of the clients connected.  
`obj`: The `pyxelobj.obj` e.g. `obj=pyxelobj.obj()`  
### Data  
* `variables`  
A class of all of the global variables.  
  Note: The class will not be created if no global variables are specified in `self.run()`  
e.g.  
`variables.Name = "Value"`  
### Users  
* `Users.__getuser__(user)`  
Returns the User's class.  
`user`: The name of the user e.g. `user="Name"`  
* `Users.__getallusers__()`  
Returns all of the Users in a dictionary in a format like this: `{"Name": <Class>, "Name": <Class>, ...}`  
### User
* `User.variables`
A class of all of the user's variables.  
* `User.key`
The user's key.  
* `User.input`  
A dictionary of all of the keys pressed in a format like this: `{"Button Number": Bool, "Button Number": Bool, ...}`  
  Note: In the client, you must use `btnp(button)` for `User.input` to update.  
## client
### Connection
* `run(Host, Port)`  
Initializes the client with necessary information.  
`Host`: The ip or domain of the server. e.g. `Host="127.0.0.1"`  
`Port`: The port to be opened in the `Host`. e.g. `Port="5000"`  
  Note: You must run this command before anything that needs to use the `client`.  
* `connect(Username)`  
Connects the client to the necessary information.  
`User`: The username e.g. `User="Name"`  
  Note: You must run this command after `run` before using anything from the `client`.  
* `request.post(Route, json)`  
Posts data to a specified route and returns json back.  
`Route`: The path to post e.g. `Route="/var"`  
`json`: The json to post to the `Route` e.g. `json={"Name": "Value"}`  
### Data
* `getGlobalvar(Variable, [Value])`  
Returns & optionaly changes a global variable from the server.  
`Variable`: The variable name e.g. `Variable="Name"`  
`Value`: The value of variable e.g. `Value="Value"`  
  Note: The variable will be changed before it returns.  
* `getLocalvar(Variable, [Value])`  
Returns & optionaly changes a local variable only accessible to the client from the server.  
`Variable`: The variable name e.g. `Variable="Name"`  
`Value`: The value of variable e.g. `Value="Value"`  
  Note: The variable will be changed before it returns.  
### Input
* `btnp(button)`  
Checks for a button press [(see pyxel documentation)](https://github.com/kitao/pyxel#input) then sends result to the server and returns result  
`button`: The button to press e.g. `button=pyxel.KEY_SPACE`  
* `btnr(button)`  
Checks for a button release [(see pyxel documentation)](https://github.com/kitao/pyxel#input) then sends result to the server and returns result  
`button`: The button to press e.g. `button=pyxel.KEY_SPACE`  
### Objects  
* `renderAll()`  
Renders all of the objects in `client.objects`  
* `addObject(obj)`  
Adds an object to `client.objects`  
`obj`: The `pyxelobj.obj` e.g. `obj=pyxelobj.obj()`  
* `addObject(objname)`  
Removes an object from `client.objects`  
* `predict(obj)`  
Predicts an object's next location by adding `obj.addX` to `obj.x` and `obj.addY` to `obj.y`  
`obj`: The `pyxelobj.obj` e.g. `obj=pyxelobj.obj(json)`  
Removes an object from `client.objects`  
`objname`: The name of the object to remove e.g. `objname="Name"`  
# Used software
* [python3](https://python.org)
* [pyxel](https://github.com/kitao/pyxel)  
* [flask](https://flask.palletsprojects.com)  
* [requests](https://docs.python-requests.org)  
