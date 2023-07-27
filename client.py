from message import Message
import json, socket


def send(host: str, port: int, data: dict):
    """
    Send message to port on host.

        Parameters:
            host (str)
            port (int)
            data (dict)

        Returns:
            status (dict): Returns response from server, if any.
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.settimeout(60)
    s.send(json.dumps(data).encode())
    fragments = []
    while True:
        chunk = s.recv(1024)
        fragments.append(chunk)
        if len(chunk) < 1024:
            break
    s.shutdown(socket.SHUT_RDWR)
    status = json.loads((b"".join(fragments)).decode("ascii"))
    return status


class Client:
    @classmethod
    def authenticate(cls, host: int, port: int, username: str, password: str):
        status = send(
            host, port, {"route": "auth", "username": username, "password": password}
        )
        return status

    @classmethod
    def signup(cls, host: int, port: int, username: str, password: str):
        status = send(
            host, port, {"route": "signup", "username": username, "password": password}
        )
        return status["uuid"]

    def __init__(
        self,
        username: str,
        password: str,
        uuid: str,
        ip_address: str,
        host: str,
        port: int,
    ):
        self.username = username
        self.password = password
        self.uuid = uuid
        self.ip_address = ip_address
        self.host = host
        self.port = port
        self.chatroom = None

    def __dict__(self):
        return {
            "username": self.username,
            "ip_address": self.ip_address,
        }

    def create(self, name: str):
        status = send(
            self.host,
            self.port,
            {
                "route": "create",
                "username": self.username,
                "password": self.password,
                "name": name,
            },
        )
        if status["code"] != 200:
            raise Exception(status["reason"])
        self.chatroom = status["chatroom_id"]

    def join(self, chatroom_id: str):
        status = send(
            self.host,
            self.port,
            {
                "route": "join",
                "username": self.username,
                "password": self.password,
                "chatroom_id": chatroom_id,
            },
        )
        return status["code"] == 200

    def send(self, msg: str):
        return send(
            self.host,
            self.port,
            {
                "route": "chat",
                "username": self.username,
                "password": self.password,
                "chatroom_id": self.chatroom,
                "msg": msg,
            },
        )
