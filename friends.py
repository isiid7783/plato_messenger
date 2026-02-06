from crypto import sign
from storage import load, save
import datetime

def add_friend(identity, friend_sign_pub, friend_box_pub):
    friends = load("friends")
    signature = sign(identity["signing_private"], friend_sign_pub)

    friends[friend_sign_pub] = {
        "box_public": friend_box_pub,
        "trust_level": 2,
        "signature": signature,
        "added": str(datetime.datetime.utcnow())
    }

    save("friends", friends)

def get_friends():
    return load("friends")
