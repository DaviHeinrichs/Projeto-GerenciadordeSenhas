import secrets

def salt_gen():
    salt = secrets.token_hex(16)
    return salt
    