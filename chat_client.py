from os import system
from sys import argv, exit
from client import Client
from colors import Colors

host = "10.29.83.169"
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
    color = Colors.random()

    authenticate = Client.authenticate(host, port, username, password)
    if authenticate["status"] is None:
        # Sign user up for an account
        uuid = Client.signup(host, port, username, password, color)
        print(f"{Colors.BOLD}~ Signed up for an account{Colors.ENDC}")
    elif not authenticate["status"]:
        print(f"{Colors.BOLD}~ Invalid password. Try again?{Colors.ENDC}")
        exit(0)
    else:
        uuid = authenticate

    client = Client(username, password, uuid, color, "0.0.0.0", host, port)

    join = None
    try:
        while join is None:
            join = int(
                input(f"{Colors.BOLD}~ Join or create chatroom (1/2): {Colors.ENDC}")
            )
            if join not in [1, 2]:
                join = None
    except ValueError:
        join = None

    if join == 1:
        # Join chatroom
        chatroom_id = None
        while chatroom_id is None:
            chatroom_id = input(f"{Colors.BOLD}~ Chatroom ID: {Colors.ENDC}")
            connected = client.join(chatroom_id)
            if not connected:
                print(f"{Colors.BOLD}~ Invalid chatroom ID, try again? {Colors.ENDC}")
                chatroom_id = None
        print(f"{Colors.BOLD}~ Joined chatroom{Colors.ENDC}")
        display_messages(connected)
    elif join == 2:
        # Create chatroom
        name = input(f"{Colors.BOLD}~ Name of chatroom: {Colors.ENDC}")
        client.create(name)
        print(f"{Colors.BOLD}~ Created chatroom{Colors.ENDC}")

    while True:
        try:
            msg = input("")
            status = client.send(msg)
        except KeyboardInterrupt:
            print(f"{Colors.BOLD}~ KeyboardInterrupt, shutting down{Colors.ENDC}")
            client.signout()
        except Exception as e:
            print(
                f"{Colors.BOLD}~ Whoops, something caused the client to crash:{Colors.ENDC}",
                e,
            )
            client.signout()
