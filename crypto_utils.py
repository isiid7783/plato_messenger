from nacl.public import PrivateKey, PublicKey, Box
from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import HexEncoder
import json
import base64

def generate_identity():
    signing_key = SigningKey.generate()
    verify_key = signing_key.verify_key
    private_key = PrivateKey.generate()
    public_key = private_key.public_key

    return {
        "signing_private": signing_key.encode(encoder=HexEncoder).decode(),
        "signing_public": verify_key.encode(encoder=HexEncoder).decode(),
        "box_private": private_key.encode(encoder=HexEncoder).decode(),
        "box_public": public_key.encode(encoder=HexEncoder).decode()
    }

def sign_data(signing_private_hex, data: str):
    signing_key = SigningKey(signing_private_hex, encoder=HexEncoder)
    signed = signing_key.sign(data.encode())
    return base64.b64encode(signed).decode()

def verify_signature(signing_public_hex, signed_data_b64):
    verify_key = VerifyKey(signing_public_hex, encoder=HexEncoder)
    signed = base64.b64decode(signed_data_b64)
    try:
        verified = verify_key.verify(signed)
        return verified.decode()
    except:
        return None

def encrypt_message(sender_private_hex, recipient_public_hex, message: str):
    sender_private = PrivateKey(sender_private_hex, encoder=HexEncoder)
    recipient_public = PublicKey(recipient_public_hex, encoder=HexEncoder)
    box = Box(sender_private, recipient_public)
    encrypted = box.encrypt(message.encode())
    return base64.b64encode(encrypted).decode()

def decrypt_message(receiver_private_hex, sender_public_hex, encrypted_b64):
    receiver_private = PrivateKey(receiver_private_hex, encoder=HexEncoder)
    sender_public = PublicKey(sender_public_hex, encoder=HexEncoder)
    box = Box(receiver_private, sender_public)
    encrypted = base64.b64decode(encrypted_b64)
    decrypted = box.decrypt(encrypted)
    return decrypted.decode()

          
