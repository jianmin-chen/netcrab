from datetime import datetime


class Message:
    sender: str
    payload: str
    chatroom_id: str
    uuid: str
    timestamp = datetime.now()

    def __init__(self, sender, payload, chatroom_id, uuid):
        self.sender = sender
        self.payload = payload
        self.chatroom_id = chatroom_id
        self.uuid = uuid

    def __str__(self):
        return (
            self.sender
            + ": "
            + self.uuid
            + "\n"
            + self.chatroom_id
            + "\n"
            + self.payload
            + "\n"
            + self.timestamp
        )
