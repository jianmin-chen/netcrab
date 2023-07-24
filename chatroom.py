from message import Message
import json


class Chatroom:
    name: str
    uuid: str
    messages: list

    def __init__(self, name: str, uuid: str):
        self.name = name
        self.uuid = uuid
        try:
            with open(f"{self.uuid}_messages.json", "r") as f:
                messages = json.loads(f.read())
                self.messages = messages
        except:
            # Chatroom database doesn't exist yet, so create a new file
            with open(f"{self.uuid}_messages.json", "w") as f:
                f.write("[]")
                self.messages = []

    def update_db(self):
        """
        Update database with current messages.
        """
        with open(f"{self.uuid}_messages.json", "w") as f:
            f.write(json.dumps(self.messages))

    def add_message(self, message: Message):
        """
        Add message to list of messages.

            Parameters:
                message (Message)

        """
        self.messages.append(message)
        self.update_db()
