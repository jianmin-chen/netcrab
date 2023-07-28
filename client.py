from message import Message
import json, socket, threading


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
    status = json.loads((b"".join(fragments)).decode("ascii"))
    return status, s


class Client:
    @classmethod
    def authenticate(cls, host: int, port: int, username: str, password: str):
        status, s = send(
            host, port, {"route": "auth", "username": username, "password": password}
        )
        s.shutdown(socket.SHUT_RDWR)
        return status

    @classmethod
    def signup(cls, host: int, port: int, username: str, password: str):
        status, s = send(
            host, port, {"route": "signup", "username": username, "password": password}
        )
        s.shutdown(socket.SHUT_RDWR)
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

    def listen(self, s: socket.socket):
        """
        Continously listen for messages from the server in case of new messages.
        """

        fragments = []
        while True:
            chunk = s.recv(1024)
            if chunk:
                fragments.append(chunk.decode("ascii"))
                if fragments[-1].endswith("}"):
                    msg = json.loads("".join(fragments))
                    if msg["username"] != self.username:
                        print(msg["new"])
                        print("> ", end="")
                    fragments = []

    def create(self, name: str):
        status, s = send(
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
            s.shutdown(socket.SHUT_RDWR)
            raise Exception(status["reason"])
        thread = threading.Thread(target=self.listen, args=(s,))
        thread.daemon = True
        thread.start()
        self.chatroom = status["chatroom_id"]

    def join(self, chatroom_id: str):
        status, s = send(
            self.host,
            self.port,
            {
                "route": "join",
                "username": self.username,
                "password": self.password,
                "chatroom_id": chatroom_id,
            },
        )
        if status["code"] == 200:
            self.chatroom = chatroom_id
            thread = threading.Thread(target=self.listen, args=(s,))
            thread.daemon = True
            thread.start()
            return status["msgs"]
        s.shutdown(socket.SHUT_RDWR)
        return False

    def send(self, msg: str):
        status, s = send(
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
        s.shutdown(socket.SHUT_RDWR)
