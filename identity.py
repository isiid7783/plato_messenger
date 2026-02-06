from crypto import generate_keys
from storage import save, load

def init_identity():
    identity = load("identity")
    if identity:
        return identity
    identity = generate_keys()
    save("identity", identity)
    return identity
