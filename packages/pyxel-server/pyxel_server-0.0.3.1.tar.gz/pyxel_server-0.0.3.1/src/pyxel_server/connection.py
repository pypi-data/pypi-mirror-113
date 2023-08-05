from flask import Flask, request
from requests import post as requests_post
from json import loads as json_loads
from threading import Thread
from secrets import token_urlsafe
from time import sleep
class webhost:
    def send(self, json, address):
        requests_post(address + "/return/" + json_loads(request.data)["return-key"], json=json)

    def run(self):
        app = Flask("webhost")

        self.web(app)
        # If debug set to true running flask on a seperate thread will not work
        # Runs on host and port
        app.run(host=self.host, port=self.port, debug=False)
        
    def __init__(self, Host:str, Port:str, Web):
        self.web = Web
        self.port = Port
        self.host = Host
        self.webhostProccess = Thread(target=self.run, daemon=True)
        self.webhostProccess.start()
class webrequest:
    def waitData(self, return_key: str):
        while return_key in self.return_data.keys():
            if self.return_data[return_key] == {}:
                sleep(0.1)
            else:
                data = self.return_data[return_key]
                self.return_data.pop(return_key)
                return data
    
    def post(self, Route, json):
        return_key = token_urlsafe(32)
        self.return_data[return_key] = {}
        json["return-key"] = return_key
        json["return-address"] = "http://" + self.host + ":" + self.port
        requests_post(self.server + str(Route), json=json)
        return self.waitData(return_key)
    
    def __init__(self, Host, Port, Server):
        self.return_data = {}
        self.host = Host
        self.port = Port
        self.server = Server