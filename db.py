from colors import Colors
import json, hashlib, pprint


def exists(uuid: str):
    """
    Determine if uuid is unique.

        Parameters:
            uuid (str)

        Returns:
            exists (bool)
    """

    with open("clients.json") as f:
        db = json.loads(f.read())
        for client in db:
            if client["uuid"] == uuid:
                return True
        return False


def authenticate(username: str, password: str):
    """
    Authenticate user given username and password.

        Parameters:
            username (str)
            password (str)

        Returns:
            authenticated (dict|bool|None)
    """

    def check_password(plain, hashed):
        # For now, just check if they're equal
        return plain == hashed

    authenticated = None
    with open("clients.json") as f:
        db = json.loads(f.read())
        for client in db:
            if client["username"] == username and check_password(
                password, client["password"]
            ):
                # Valid user, return UUID
                authenticated = {
                    "uuid": client["uuid"],
                    "username": client["username"],
                    "color": client["color"],
                }
                break
            elif client["username"] == username and not check_password(
                password, client["password"]
            ):
                authenticated = False
                break
    return authenticated


def create(username: str, password: str, color=Colors.random()):
    """
    Creates user in database file.

    Parameters:
        username (str)
        password (str)
        color (str)
    """

    def hash_password(password):
        # Just return password for now
        return password

    uuid = hashlib.sha1(username.encode("utf-8")).hexdigest()
    db = None
    with open("clients.json", "r") as f:
        db = json.loads(f.read())
    with open("clients.json", "w") as f:
        db.append(
            {
                "username": username,
                "password": hash_password(password),
                "uuid": uuid,
                "color": color,
            }
        )
        f.write(json.dumps(db))
    return uuid


def create_chatroom(name: str):
    uuid = 0
    db = None
    with open("chatrooms.json") as f:
        db = json.loads(f.read())
        uuid = len(db.keys())
        with open(f"{uuid}_messages.json", "w") as chatroom:
            chatroom.write("[]")
        db[uuid] = name
    with open("chatrooms.json", "w") as f:
        f.write(json.dumps(db))
    return uuid


def chatroom_exists(uuid: str):
    with open("chatrooms.json") as f:
        db = json.loads(f.read())
        if uuid in db.keys():
            return True
        return False


def chatroom_name(uuid: str):
    with open("chatrooms.json") as f:
        db = json.loads(f.read())
        return db[uuid]


def get_chatroom(uuid: str):
    with open(f"{uuid}_messages.json") as f:
        messages = json.loads(f.read())
        return messages


def update_chatroom(uuid: str, messages):
    messages = [str(message) for message in messages]
    with open(f"{uuid}_messages.json", "w") as f:
        f.write(json.dumps(messages))
