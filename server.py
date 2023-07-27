import json, socket, threading


class Server:
    def __init__(self, host: str, port: int, backlog: int = 10, bufsize: int = 1024):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.bufsize = bufsize
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))

    def close(self):
        """
        Close socket.
        """

        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except:
            pass

    def listen(self):
        self.socket.listen(self.backlog)
        while True:
            client, address = self.socket.accept()
            client.settimeout(60)
            threading.Thread(target=self.receive, args=(client, address)).start()

    def receive(self, client, address):
        try:
            fragments = []
            while True:
                chunk = client.recv(self.bufsize)
                fragments.append(chunk)
                if len(chunk) < self.bufsize:
                    break
            self.respond(
                client, address, json.loads((b"".join(fragments)).decode("ascii"))
            )
        except Exception as e:
            self.send(client, {"code": 500, "reason": str(e)})

    def respond(self, client, address, data):
        self.send(client, {"response": "received"})

    def send(self, client, data: dict):
        client.send(json.dumps(data).encode())


def available_port(start: int, max_search: int = 10):
    """
    Test for available ports, starting from given argument.

    Parameters:
        start (int)

    Returns:
        available (int)
    """

    available = start
    query = 0
    while query < max_search:
        # Search for available ports
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind(("0.0.0.0", available))
            s.close()
            return available
        except:
            s.close()
            available += 1
            query += 1
    raise Exception(f"Unable to find available port from range {start} to {available}.")
