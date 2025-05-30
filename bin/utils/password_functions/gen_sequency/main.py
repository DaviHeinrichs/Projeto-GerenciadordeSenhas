import secrets
import string
import random

def gen_sequency ():
    options = string.ascii_lowercase + string.ascii_uppercase + string.digits + "!@#$%&"
    senha = ""
    senha_max = 1
    
    while senha_max<=12:
        senha+=(secrets.choice(options))
        senha_max +=1
    
    return senha

def sequency_mixer(senha):
    options = list(senha)
    random.shuffle(options)
    return ''.join(options)
