from copy import deepcopy
from json import load as json_load
from pyxel import pset
import pyxel

TEMPLATE = {
    "name": "",
    "render": {
        "width": 1,
        "height": 1,
        "x": 0,
        "y": 0,
        "addX": 0,
        "addY": 0,
        "image": [
        ]
    }
}

class obj:
    def __init__(self, pyxelobj):
        self.name = str(pyxelobj["name"])
        self.x = int(pyxelobj["render"]["x"])
        self.y = int(pyxelobj["render"]["y"])
        self.addX = int(pyxelobj["render"]["addX"])
        self.addY = int(pyxelobj["render"]["addY"])
        self.width = int(pyxelobj["render"]["width"])
        self.height = int(pyxelobj["render"]["height"])
        self.image = list(pyxelobj["render"]["image"])

def new(name: str, x:int, y:int, addX:int, addY:int, image:list):
    pyxelobj = deepcopy(TEMPLATE)
    pyxelobj["name"] = name
    pyxelobj["render"]["x"] = x
    pyxelobj["render"]["y"] = y
    pyxelobj["render"]["addX"] = addX
    pyxelobj["render"]["addY"] = addY
    pyxelobj["render"]["width"] = len(image[0])
    pyxelobj["render"]["height"] = len(image)
    pyxelobj["render"]["image"] = image
    return pyxelobj

def load(File):
    return json_load(File.read())

def render(pyxelobj: obj):
    for y in range(pyxelobj.height):
        for x in range(pyxelobj.width):
            pset(x + pyxelobj.x, y + pyxelobj.y, pyxelobj.image[y][x])