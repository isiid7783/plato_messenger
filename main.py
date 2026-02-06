from crypto_utils import *
from storage import *
import json
import datetime

def init_identity():
    identity = load_identity()
    if identity:
        return identity
    print("Creating new identity...")
    identity = generate_identity()
    save_identity(identity)
    return identity

def add_friend(identity):
    friends = load_friends()
    friend_signing_pub = input("Friend signing public key: ")
    friend_box_pub = input("Friend box public key: ")

    signature = sign_data(identity["signing_private"], friend_signing_pub)

    friends[friend_signing_pub] = {
        "box_public": friend_box_pub,
        "signature": signature,
        "trust_level": 2,
        "timestamp": str(datetime.datetime.utcnow())
    }

    save_friends(friends)
    print("Friend added with signature.")

def list_friends():
    friends = load_friends()
    for k in friends:
        print("Friend:", k[:16], "... Trust:", friends[k]["trust_level"])

def send_message(identity):
    friends = load_friends()
    friend_key = input("Friend signing public key: ")

    if friend_key not in friends:
        print("Not a trusted friend.")
        return

    message = input("Message: ")
    encrypted = encrypt_message(
        identity["box_private"],
        friends[friend_key]["box_public"],
        message
    )

    messages = load_messages()
    if friend_key not in messages:
        messages[friend_key] = []

    messages[friend_key].append({
        "direction": "out",
        "content": encrypted,
        "timestamp": str(datetime.datetime.utcnow())
    })

    save_messages(messages)
    print("Encrypted message stored locally.")

def read_messages(identity):
    messages = load_messages()
    friends = load_friends()

    for friend_key in messages:
        print("Conversation with:", friend_key[:16], "...")
        for msg in messages[friend_key]:
            if msg["direction"] == "out":
                print("You:", decrypt_message(
                    identity["box_private"],
                    friends[friend_key]["box_public"],
                    msg["content"]
                ))
            else:
                print("Friend:", msg["content"])

def menu():
    identity = init_identity()
    print("Your signing public key:", identity["signing_public"])
    print("Your box public key:", identity["box_public"])

    while True:
        print("\n1 Add Friend")
        print("2 List Friends")
        print("3 Send Message")
        print("4 Read Messages")
        print("5 Exit")

        choice = input("> ")

        if choice == "1":
            add_friend(identity)
        elif choice == "2":
            list_friends()
        elif choice == "3":
            send_message(identity)
        elif choice == "4":
            read_messages(identity)
        elif choice == "5":
            break

if __name__ == "__main__":
    ensure_data_dir()
    menu()

