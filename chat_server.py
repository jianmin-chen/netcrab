from server import Server, available_port
from sys import exit

if __name__ == "__main__":
    port = available_port(5000)
    print("Listening on port:", port)

    server = Server("0.0.0.0", port)

    try:
        server.listen()
    except KeyboardInterrupt:
        server.close()
        print("InterruptError, shutting down")
    except Exception as e:
        server.close()
        print("Whoops, something caused the server to crash:", e)
