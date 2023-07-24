from config import DEBUG
from chatroom import Chatroom
from message import Message
from server import available_port, Server
from sys import exit

chatroom_name = "BWSI AUV Chat"
chatroom_id = "bwsi-auv-chat"

if __name__ == "__main__":
    chatroom = Chatroom(chatroom_name, chatroom_id)

    port = available_port(5000)
    server = Server("0.0.0.0", port)
    if DEBUG:
        print("Listening on port:", port)

    while True:
        # Start listening for requests
        try:
            data, connection = server.receive()
            # Now pass data to be used for something
            if data is not None:
                """
                Take data, which is a JSON payload, and upload to chatroom.
                If successful, return 200; otherwise, return 500.
                """
                chatroom.add_message(
                    Message(data["sender"], data["payload"], chatroom.uuid)
                )
                connection.sendall()
        except KeyboardInterrupt:
            server.close()
            print("KeyboardInterrupt: Server shut down")
            exit(0)
        except Exception as e:
            print("Whoops, something caused the server to crash:", e)
