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
    try:
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
    except:
        s.shutdown(socket.SHUT_RDWR)


def authenticate(username: str, password: str):
    pass


class Client:
    def __init__(self, username: str, password: str, ip_address: str):
        self.username = username
        self.password = password
        self.ip_address = ip_address

        auth = authenticate(self.username, self.password)

    def __dict__(self):
        return {
            "username": self.username,
            "ip_address": self.ip_address,
        }

    def send(self, host: str, port: int, chatroom_id: str, msg: str):
        return send(host, port, {"msg": msg})
