from datetime import datetime


class Message:
    def __init__(
        self,
        sender: str,
        payload: str,
        chatroom_id,
        uuid,
        timestamp=datetime.now(),
    ):
        self.sender = sender
        self.payload = payload
        self.chatroom_id = chatroom_id
        self.uuid = uuid
        self.timestamp = timestamp

    def __str__(self):
        return f"{self.sender} at {self.timestamp}: {self.payload}"
