from config import DEBUG
import socket


class Server:
    def __init__(
        self, ip_address: str, port: int, max_connections: int = 10, bufsize: int = 1024
    ):
        self.ip_address = ip_address
        self.port = port
        self.max_connections = max_connections
        self.bufsize = bufsize
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip_address, self.port))
        self.socket.setblocking(False)
        self.socket.listen(max_connections)

    def close(self):
        """
        Close socket.
        """

        self.socket.shutdown(socket.SHUT_RDWR)

    def receive(self, decode_as: str = "ascii"):
        """
        Receive data being sent from a client.
        """

        connection = None
        try:
            connection, address = self.socket.accept()
            fragments = []
            while True:
                chunk = connection.recv(self.bufsize)
                fragments.append(chunk)
                if len(chunk) < self.bufsize:
                    break
            connection.close()
            return (b"".join(fragments)).decode(decode_as).strip()
        except BlockingIOError:
            if connection is not None:
                connection.close()
            return None


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
