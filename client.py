from uuid import uuid4
from message import Message
import json, socket


def exists(uuid: str):
    """
    Determine if uuid is unique.

        Parameters:
            uuid (str)

        Returns:
            exists (bool)
    """

    with open("clients.json") as f:
        db = json.loads(f.read())
        for client in db:
            if client["uuid"] == uuid:
                return True
        return False


def authenticate(username: str, password: str):
    """
    Authenticate user given username and password.

        Parameters:
            username (str)
            password (str)

        Returns:
            authenticated (dict|bool|None)
    """

    authenticated = None
    with open("clients.json") as f:
        db = json.loads(f.read())
        for client in db:
            if client["username"] == username and client["password"] == password:
                authenticated = {"uuid": client["uuid"]}
                break
            elif client["username"] == username and client["password"] != password:
                authenticated = False
                break
    return authenticated


def create(username: str, password: str, uuid: str):
    """
    Creates user in database file.

    Parameters:
        username (str)
        password (str)
        uuid (str)
    """

    with open("clients.json", "r+w") as f:
        db = json.loads(f.read())
        db.append({"username": username, "password": password, "uuid": uuid})
        f.write(db)


class Client:
    username: str
    password: str
    ip_address: str
    uuid: str

    def __init__(
        self, username: str, password: str, ip_address: str, bufsize: int = 1024
    ):
        self.username = username
        self.password = password
        self.ip_address = ip_address
        self.bufsize = bufsize

        auth = authenticate(self.username, self.password)
        if auth is None:
            self.uuid = uuid4()
            while exists(self.uuid):
                self.uuid = uuid4()
            create(self.username, self.password, self.uuid)
        elif not auth:
            raise Exception("Incorrect password, try again!")
        else:
            self.uuid = auth["uuid"]

    def __dict__(self):
        return {
            "username": self.username,
            "ip_address": self.ip_address,
            "uuid": self.uuid,
        }

    def send(self, host: str, port: int, msg: str, decode_as: str = "ascii"):
        """
        Send message to port on host.

            Parameters:
                host (str)
                port (int)
                msg (str)

            Returns:
                status (dict): Returns a status dict containing the status code and potential error reason.
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((host, port))
            payload = Message(self.username, msg, self.uuid)
            s.sendall(bytes(payload))
            fragments = []
            while True:
                chunk = s.recv(self.bufsize)
                fragments.append(chunk)
                if len(chunk) < self.bufsize:
                    break
            s.shutdown(socket.SHUT_RDWR)
            status = json.loads((b"".join(fragments)).decode(decode_as))
            return status
        finally:
            s.shutdown(socket.SHUT_RDWR)
