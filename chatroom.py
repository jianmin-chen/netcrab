from db import get_chatroom, create_chatroom, update_chatroom
from message import Message


class Chatroom:
    def __init__(self, name: str, uuid: str, connections: list = []):
        self.name = name
        self.uuid = uuid
        self.connections = connections

        try:
            self.messages = get_chatroom(self.uuid)
        except:
            # Chatroom database doesn't exist yet, so create a new one
            self.messages = create_chatroom(self.uuid)

    def add_message(self, message: Message):
        self.messages.append(message)
        update_chatroom(self.uuid, self.messages)
