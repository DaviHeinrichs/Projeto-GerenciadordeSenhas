import secrets
import string

def Gen_Sequency ():
    options = string.ascii_lowercase + string.ascii_uppercase + string.digits + "!@#$%&"
    senha = ""
    senha_max = 1
    
    while senha_max<=12:
        senha+=(secrets.choice(options))
        senha_max +=1
    
    return senha
