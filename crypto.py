from nacl.public import PrivateKey, PublicKey, Box
from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import HexEncoder
import base64

def generate_keys():
    signing_key = SigningKey.generate()
    verify_key = signing_key.verify_key
    box_private = PrivateKey.generate()
    box_public = box_private.public_key

    return {
        "signing_private": signing_key.encode(HexEncoder).decode(),
        "signing_public": verify_key.encode(HexEncoder).decode(),
        "box_private": box_private.encode(HexEncoder).decode(),
        "box_public": box_public.encode(HexEncoder).decode()
    }

def sign(private_hex, data):
    sk = SigningKey(private_hex, encoder=HexEncoder)
    signed = sk.sign(data.encode())
    return base64.b64encode(signed).decode()

def verify(public_hex, signed_b64):
    vk = VerifyKey(public_hex, encoder=HexEncoder)
    try:
        data = vk.verify(base64.b64decode(signed_b64))
        return data.decode()
    except:
        return None

def encrypt(sender_priv_hex, recipient_pub_hex, message):
    sender_priv = PrivateKey(sender_priv_hex, encoder=HexEncoder)
    recipient_pub = PublicKey(recipient_pub_hex, encoder=HexEncoder)
    box = Box(sender_priv, recipient_pub)
    return base64.b64encode(box.encrypt(message.encode())).decode()

def decrypt(receiver_priv_hex, sender_pub_hex, encrypted_b64):
    receiver_priv = PrivateKey(receiver_priv_hex, encoder=HexEncoder)
    sender_pub = PublicKey(sender_pub_hex, encoder=HexEncoder)
    box = Box(receiver_priv, sender_pub)
    return box.decrypt(base64.b64decode(encrypted_b64)).decode()
