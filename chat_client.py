from sys import argv, exit
from client import Client

host = "10.0.0.81"
port = 5000

if __name__ == "__main__":
    if len(argv) != 3:
        print("Usage: python chat_client.py <username> <password>")
        exit(0)

    username = argv[1]
    password = argv[2]

    authenticate = Client.authenticate(host, port, username, password)
    if authenticate["status"] is None:
        # Sign user up for an account
        uuid = Client.signup(host, port, username, password)
    elif not authenticate["status"]:
        print("Invalid password. Try again?")
        exit(0)
    else:
        uuid = authenticate

    client = Client(username, password, uuid, "0.0.0.0")

    while True:
        try:
            msg = input("> ")
            status = client.send(host, port, 0, msg)
            print(status)
        except KeyboardInterrupt:
            print("KeyboardInterrupt, shutting down")
            exit(0)
        except Exception as e:
            print("Whoops, something caused the client to crash:", e)
            exit(-1)
