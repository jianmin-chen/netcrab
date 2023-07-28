from os import system
from sys import argv, exit
from client import Client

host = "10.0.0.81"
port = 5000


def display_messages(messages):
    print("\n".join(messages))


if __name__ == "__main__":
    if len(argv) != 3:
        print("Usage: python chat_client.py <username> <password>")
        exit(0)

    system("clear")

    username = argv[1]
    password = argv[2]

    authenticate = Client.authenticate(host, port, username, password)
    if authenticate["status"] is None:
        # Sign user up for an account
        uuid = Client.signup(host, port, username, password)
        print("~ Signed up for an account")
    elif not authenticate["status"]:
        print("~ Invalid password. Try again?")
        exit(0)
    else:
        uuid = authenticate

    client = Client(username, password, uuid, "0.0.0.0", host, port)

    join = None
    try:
        while join is None:
            join = int(input("~ Join or create chatroom (1/2): "))
            if join not in [1, 2]:
                join = None
    except ValueError:
        join = None

    if join == 1:
        # Join chatroom
        chatroom_id = None
        while chatroom_id is None:
            chatroom_id = input("~ Chatroom ID: ")
            connected = client.join(chatroom_id)
            if not connected:
                print("~ Invalid chatroom ID, try again? ")
                chatroom_id = None
        print("~ Joined chatroom")
        display_messages(connected)
    elif join == 2:
        # Create chatroom
        name = input("~ Name of chatroom: ")
        client.create(name)
        print("~ Created chatroom")

    while True:
        try:
            msg = input("> ")
            status = client.send(msg)
        except KeyboardInterrupt:
            print("~ KeyboardInterrupt, shutting down")
            exit(0)
        except Exception as e:
            print("~ Whoops, something caused the client to crash:", e)
            exit(-1)
