import json, hashlib


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
                authenticated = {"uuid": client["uuid"]}
                break
            elif client["username"] == username and not check_password(
                password, client["password"]
            ):
                authenticated = False
                break
    return authenticated


def create(username: str, password: str):
    """
    Creates user in database file.

    Parameters:
        username (str)
        password (str)
    """

    def hash_password(password):
        # Just return password for now
        return password

    uuid = hashlib.sha1(username.encode("utf-8")).hexdigest()
    with open("clients.json", "r+w") as f:
        db = json.loads(f.read())
        db.append(
            {
                "username": username,
                "password": hash_password(password),
                "uuid": uuid,
            }
        )
        f.write(db)
    return uuid


def create_chatroom(uuid: str):
    with open(f"{uuid}_messages.json", "w") as f:
        f.write("[]")
    return []


def get_chatroom(uuid: str):
    with open(f"{uuid}_messages.json") as f:
        messages = json.loads(f.read())
        return messages


def update_chatroom(uuid: str, messages):
    messages = [str(message) for message in messages]
    with open(f"{uuid}_messages.json", "w") as f:
        f.write(json.dumps(messages))
