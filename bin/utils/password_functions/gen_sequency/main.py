import secrets
import string
import random

def gen_sequency ():
    maiúsculas = string.ascii_uppercase
    minúsculas = string.ascii_lowercase
    digitos = string.digits 
    especiais = "!@#$%&"
    
    options = minúsculas + maiúsculas + digitos + especiais
    
    senha = ""
    senha += secrets.choice(minúsculas)
    senha += secrets.choice(maiúsculas)
    senha += secrets.choice(digitos)
    senha += secrets.choice(especiais)
    
    senha_contador = 4

    while senha_contador<=12:
        senha+=(secrets.choice(options))
        senha_contador+=1
        
            

    return senha

def sequency_mixer(senha):
    options = list(senha)
    random.shuffle(options)
    return ''.join(options)
