import asyncio, json
from identity import init_identity
from friends import add_friend, get_friends
from network import start_server, connect_and_send
from crypto import encrypt, decrypt
from storage import load, save

identity = init_identity()

async def main():
    print("Your signing key:", identity["signing_public"])
    print("Your box key:", identity["box_public"])

    await start_server()

    while True:
        print("1 Add Friend")
        print("2 List Friends")
        print("3 Send Message")
        print("4 Exit")

        c = input("> ")

        if c == "1":
            sp = input("Friend signing pub: ")
            bp = input("Friend box pub: ")
            add_friend(identity, sp, bp)
        elif c == "2":
            print(get_friends())
        elif c == "3":
            friends = get_friends()
            target = input("Friend signing pub: ")
            msg = input("Message: ")
            encrypted = encrypt(identity["box_private"],
                                friends[target]["box_public"],
                                msg)
            payload = {
                "from": identity["signing_public"],
                "content": encrypted
            }
            uri = input("ws://ip:port : ")
            await connect_and_send(uri, payload)
        elif c == "4":
            break

if __name__ == "__main__":
    asyncio.run(main())

