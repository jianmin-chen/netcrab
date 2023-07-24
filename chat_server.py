from config import DEBUG
from server import available_port, Server
from sys import exit


if __name__ == "__main__":
    port = available_port(5000)
    server = Server("0.0.0.0", port)
    if DEBUG:
        print("Listening on port:", port)

    while True:
        # Start listening for requests
        try:
            data = server.receive()
            # Now pass data to be used for something
            if data is not None:
                print(data)
        except KeyboardInterrupt:
            server.close()
            print("KeyboardInterrupt: Server shut down")
            exit(0)
        except Exception as e:
            print("Whoops, something caused the server to crash:", e)
            exit(-1)
