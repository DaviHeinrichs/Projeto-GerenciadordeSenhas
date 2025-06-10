import secrets
import string

def gerar_id():
    options = string.digits
    id = ""
    contador = 1
    while contador<=8:
        id+=(secrets.choice(options))
        contador +=1
         
    return "".join(id)
    
        