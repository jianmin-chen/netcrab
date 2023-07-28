This is the Python version, which definitely has some questionable code. (We use files as databases and read them in full every time we need to update them, for one.)

Requirements:

* The server should be able to handle multiple clients at once.
* The server should broadcast messages to all clients.
* The server should send a message to the chatroom when a new client joins the chat room.
* The server should send a message to the chatroom when a client leaves the chat room.
* The client should be able to send messages to the server.
* The client should be able to receive messages from the server.
* The client should be able to gracefully exit the chat room.
* The client should have a username, which is sent to the server when the client joins the chat room.
* The server should keep track of all clients in the chat room.
* The client is defined by:
  * username
  * IP address
  * password
  * unique ID
* The server is defined by:
  * IP address
  * port
* A message in the chat room is defined by:
  * sender (the client ID)
  * payload (the message)
  * timestamp
  * chatroom ID
  * unique ID
* The chat room is defined by:
  * name
  * unique ID