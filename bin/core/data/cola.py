import uuid
import secrets

def criar_usuário():
    user_id = uuid.uuid4()
    user_salt = secrets.token_bytes(16)
    
    print(user_id)
    print(user_salt)
    
    
criar_usuário()