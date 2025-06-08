import uuid
import secrets

def criar_usuário():
    user_id = uuid.uuid4()
    user_salt = secrets.token_bytes(16)