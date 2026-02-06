import json
import os

DATA_DIR = "data"
IDENTITY_FILE = os.path.join(DATA_DIR, "identity.json")
FRIENDS_FILE = os.path.join(DATA_DIR, "friends.json")
MESSAGES_FILE = os.path.join(DATA_DIR, "messages.json")

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)

def save_identity(identity):
    save_json(IDENTITY_FILE, identity)

def load_identity():
    return load_json(IDENTITY_FILE)

def save_friends(friends):
    save_json(FRIENDS_FILE, friends)

def load_friends():
    data = load_json(FRIENDS_FILE)
    return data if data else {}

def save_messages(messages):
    save_json(MESSAGES_FILE, messages)

def load_messages():
    data = load_json(MESSAGES_FILE)
    return data if data else {}

