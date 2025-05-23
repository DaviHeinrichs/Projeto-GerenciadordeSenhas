import secrets
import string
import random

def Gen_Sequency ():
    options = string.ascii_lowercase + string.ascii_uppercase + string.digits + "!@#$%&"
    senha = ""
    senha_max = 1
    
    while senha_max<=12:
        senha+=(secrets.choice(options))
        senha_max +=1
    
    return senha

senha = Gen_Sequency()

def sequency_mixer(senha):
    options = list(senha)
    random.shuffle(options)
    return ''.join(options)

senha_embaralhada = sequency_mixer(senha)

print(senha)
print(senha_embaralhada)