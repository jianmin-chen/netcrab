from sys import argv, exit
from client import Client
from chatroom import Chatroom

host = "10.29.95.14"
port = "5000"

if __name__ == "__main__":
    if len(argv) != 3:
        print("Usage: python chat_client.py <username> <password>")

    username = argv[1]
    password = argv[2]

    client = Client(username, password)

    while True:
        # Start listening for messages to send
        try:
            msg = input("> ")
            # Take message, upload
            status = client.send(host, port, msg)
            if status["code"] == 500:
                raise Exception(f"Server error ~ {status['reason']}")
            display_messages()
        except Exception as e:
            print("Whoops, something caused the client to crash:", e)
            exit(-1)
