import json
from uuid import uuid4
import message

def authenticate(username, password):
    with open("clients.json") as f:
        db = json.loads(f.read()) 
        for client in db:
            if client["username"]==username and client["password"] == password:
                return True
            if client["username"]==username and client["password"] != password:
                return True
        return None

def create(username, password):
    f = open("clients.json", "a")
    f.write(json.dumps({"username": username, "password":password}))

class Client:
    # creates a client 
    username:str
    ip_address:str
    password:str
    uuid:str

    def __init__(self, username:str, password:str, ip_address:str=" "):
        self.username=username
        self.ip_address=ip_address
        self.password=password
        self.uuid=uuid4()
        #dictionary =  {"username": username, "ip_address": ip_address, "password":password, "uuid":uuid}
    
    def __dict__(self):
        return {
            "username": self.username, "ip_address": self.ip_address, "password":self.password, "uuid":self.uuid
        }
    
    def convertToJson(self):
        x =  {"username": self.username, "ip_address": self.ip_address, "password":self.password, "uuid":self.uuid
        }
        return json.dumps(x)
    
    def verifyUser(self, password:str):
        if self.password is not password:
            return False
        else:
            return True
    
    def writeFile(self):
        f = open("clients.json", "a")
        f.write()