from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import binascii

def key_gen(password,key_salt):
    salt_hex = key_salt
    salt_bytes = bytes.fromhex(salt_hex)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt = salt_bytes,
        iterations=100000,
        backend=default_backend()
    )
    password_bytes = password.encode('utf-8')
    key = kdf.derive(password_bytes)
    
    return key



def verification_hash_create(password,used_salt):
    salt_hex = used_salt
    salt_bytes = bytes.fromhex(salt_hex)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt = salt_bytes,
        iterations=100000,
        backend=default_backend()
    )
    password_bytes = password.encode('utf-8')
    hash_bytes = kdf.derive(password_bytes)
    hash_hex = binascii.hexlify(hash_bytes).decode('utf-8')
    
    return hash_hex



def master_verify(password, used_salt,stored_hash_hex):
    salt_hex = used_salt
    salt_bytes = bytes.fromhex(salt_hex)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt = salt_bytes,
        iterations=100000,
        backend=default_backend()
    )
    password_bytes = password.encode('utf-8')
    stored_hash_bytes = bytes.fromhex(stored_hash_hex)
    try:
        kdf.verify(password_bytes, stored_hash_bytes)
        return True
    except Exception:
        return False
